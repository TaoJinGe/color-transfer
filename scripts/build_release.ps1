param([switch]$SkipTests)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
$targets = @("build", "dist", "release") | ForEach-Object { Join-Path $projectRoot $_ }

if (-not (Test-Path -LiteralPath $python)) {
    throw "Project virtual environment was not found. Run start.bat first."
}
if (-not $SkipTests) {
    & $python -m pytest -q -p no:cacheprovider
    if ($LASTEXITCODE -ne 0) { throw "Tests failed; release build stopped." }
}
foreach ($target in $targets) {
    if ((Test-Path -LiteralPath $target) -and $target.StartsWith($projectRoot)) {
        Remove-Item -LiteralPath $target -Recurse -Force
    }
}
Push-Location $projectRoot
try {
    & $python -m PyInstaller --noconfirm "ColorTransfer.spec"
    if ($LASTEXITCODE -ne 0) { throw "PyInstaller build failed." }

    $basePython = (& $python -c "import sys; print(sys.base_prefix)").Trim()
    $runtimeDir = Join-Path $projectRoot "dist\ColorTransfer\runtime"
    $runtimeLib = Join-Path $runtimeDir "Lib"
    $appDir = Join-Path $projectRoot "dist\ColorTransfer\app"
    New-Item -ItemType Directory -Force $runtimeDir, $appDir | Out-Null
    Copy-Item -LiteralPath (Join-Path $basePython "DLLs") -Destination $runtimeDir -Recurse
    Copy-Item -LiteralPath (Join-Path $basePython "Lib") -Destination $runtimeDir -Recurse
    $bundledSitePackages = Join-Path $runtimeLib "site-packages"
    if ((Test-Path -LiteralPath $bundledSitePackages) -and $bundledSitePackages.StartsWith($runtimeDir)) {
        Remove-Item -LiteralPath $bundledSitePackages -Recurse -Force
    }
    Get-ChildItem -LiteralPath $basePython -File | Where-Object {
        $_.Name -like "python*.exe" -or $_.Name -like "python*.dll" -or $_.Name -like "vcruntime*.dll" -or $_.Name -eq "LICENSE.txt"
    } | Copy-Item -Destination $runtimeDir
    & $python -m pip install --disable-pip-version-check --no-compile --target $bundledSitePackages -r "requirements.txt"
    if ($LASTEXITCODE -ne 0) { throw "Portable runtime dependency installation failed." }

    Copy-Item -LiteralPath "desktop_app.py" -Destination $appDir
    Copy-Item -LiteralPath "color_transfer" -Destination $appDir -Recurse
    Get-ChildItem -LiteralPath $appDir -Directory -Recurse -Filter "__pycache__" | Remove-Item -Recurse -Force
    Copy-Item -LiteralPath "README.md" -Destination "dist\ColorTransfer\README.md"

    $selfTestLog = Join-Path $projectRoot "build\frozen-self-test.log"
    $env:COLOR_TRANSFER_SELF_TEST_LOG = $selfTestLog
    $selfTest = Start-Process -FilePath "dist\ColorTransfer\ColorTransfer.exe" -ArgumentList "--self-test" -PassThru
    if (-not $selfTest.WaitForExit(60000)) {
        Stop-Process -Id $selfTest.Id -Force
        throw "Frozen application self-test timed out."
    }
    if ($selfTest.ExitCode -ne 0) { throw "Frozen application self-test failed." }
    Remove-Item Env:COLOR_TRANSFER_SELF_TEST_LOG -ErrorAction SilentlyContinue

    $isccCandidates = @(
        "$env:LOCALAPPDATA\Programs\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles(x86)\Inno Setup 6\ISCC.exe",
        "$env:ProgramFiles\Inno Setup 6\ISCC.exe"
    )
    $iscc = $isccCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    if (-not $iscc) { throw "Inno Setup 6 compiler was not found." }
    & $iscc "installer\ColorTransfer.iss"
    if ($LASTEXITCODE -ne 0) { throw "Installer build failed." }
} finally {
    Pop-Location
}
