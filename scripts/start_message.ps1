param([Parameter(Mandatory = $true)][string]$Key)

$OutputEncoding = [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$messages = @{
    find_python = '5q2j5Zyo5p+l5om+IFB5dGhvbiAzLjExLi4u'
    create_venv = '5q2j5Zyo5Yib5bu66Jma5ouf546v5aKDLi4u'
    install_dependencies = '5q2j5Zyo5a6J6KOF6aG555uu5L6d6LWW77yM6aaW5qyh5ZCv5Yqo6ZyA6KaB6IGU572R5bm2562J5b6F5Yeg5YiG6ZKfLi4u'
    check_success = '5ZCv5Yqo546v5aKD5qOA5p+l5oiQ5Yqf44CC'
    launching = '5q2j5Zyo5ZCv5Yqo5Y+C6ICD5Zu+6Ieq5Yqo6LCD6Imy77yM6K+35Yu/5YWz6Zet5q2k56qX5Y+jLi4u'
    python_error = 'W+mUmeivr10g5pyq5om+5YiwIFB5dGhvbiAzLjEx77yM6K+36YeN5paw5a6J6KOFIFB5dGhvbiAzLjEx44CC'
    venv_error = 'W+mUmeivr10g6Jma5ouf546v5aKD5Yib5bu65aSx6LSl77yM6K+35qOA5p+l56OB55uY56m66Ze05oiW55uu5b2V5p2D6ZmQ44CC'
    dependency_error = 'W+mUmeivr10g5L6d6LWW5a6J6KOF5aSx6LSl77yM6K+35qOA5p+l572R57uc5ZCO6YeN6K+V77yb5bey5a6J6KOF546v5aKD5Y+v5pat572R5ZCv5Yqo44CC'
    launch_error = 'W+mUmeivr10g56iL5bqP5ZCv5Yqo5aSx6LSl77yM6K+35qOA5p+l5LiK5pa55o+Q56S644CC'
}
if ($messages.ContainsKey($Key)) {
    $bytes = [Convert]::FromBase64String($messages[$Key])
    Write-Host ([Text.Encoding]::UTF8.GetString($bytes))
}
