"""生成真实图片新旧算法四图对照与量化报告。"""

import argparse
import csv
import gc
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

from color_transfer.core import transfer_color_distribution
from color_transfer.lab_transfer import transfer_lab_statistics
from color_transfer.palette_distance import sliced_wasserstein_distance


def main() -> None:
    arguments = _arguments()
    files = sorted(path for path in arguments.input_dir.rglob("*") if path.suffix.lower() in {".jpg", ".jpeg", ".png"})
    if len(files) < 2:
        raise SystemExit("真实图片目录至少需要两张图片。")
    arguments.output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for offset in range(arguments.count):
        index = arguments.start_index + offset
        source_path = files[index % len(files)]
        reference_path = files[(index * 5 + 1) % len(files)]
        source = _load_rgb(source_path, arguments.max_edge)
        reference = _load_rgb(reference_path, arguments.max_edge)
        old_result = transfer_lab_statistics(source, reference, luminance_protection=0.0)
        new_result = transfer_color_distribution(source, reference)
        before = sliced_wasserstein_distance(source, reference)
        old_distance = sliced_wasserstein_distance(old_result, reference)
        new_distance = sliced_wasserstein_distance(new_result, reference)
        ratio = new_distance / max(before, 1e-9)
        passed = new_distance <= 0.001 if before <= 0.001 else ratio <= 0.35
        _save_comparison(
            arguments.output_dir / f"case_{index + 1:02d}.jpg",
            source,
            reference,
            old_result,
            new_result,
            ratio,
        )
        rows.append(
            {
                "case": index + 1,
                "source": source_path.name,
                "reference": reference_path.name,
                "before_distance": f"{before:.6f}",
                "old_distance": f"{old_distance:.6f}",
                "new_distance": f"{new_distance:.6f}",
                "new_ratio": f"{ratio:.4f}",
                "passed_35_percent": passed,
            }
        )
        del source, reference, old_result, new_result
        gc.collect()
    report_path = arguments.output_dir / f"metrics_{arguments.start_index + 1:02d}_{arguments.start_index + arguments.count:02d}.csv"
    with report_path.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.DictWriter(stream, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    passed = sum(row["passed_35_percent"] for row in rows)
    print(f"真实图片验收：{passed}/{len(rows)} 通过 35% 配色距离门槛")


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--count", type=int, default=30)
    parser.add_argument("--start-index", type=int, default=0)
    parser.add_argument("--max-edge", type=int, default=640)
    return parser.parse_args()


def _load_rgb(path: Path, max_edge: int) -> np.ndarray:
    with Image.open(path) as image:
        rgb = ImageOps.exif_transpose(image).convert("RGB")
        rgb.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
        return np.asarray(rgb, dtype=np.uint8).copy()


def _save_comparison(
    path: Path,
    source: np.ndarray,
    reference: np.ndarray,
    old_result: np.ndarray,
    new_result: np.ndarray,
    ratio: float,
) -> None:
    height, width = source.shape[:2]
    panels = [source, _fit_reference(reference, width, height), old_result, new_result]
    labels = ["SOURCE", "REFERENCE", "OLD", f"NEW ratio={ratio:.3f}"]
    sheet = Image.new("RGB", (width * 4, height + 28), "white")
    draw = ImageDraw.Draw(sheet)
    for index, (panel, label) in enumerate(zip(panels, labels)):
        sheet.paste(Image.fromarray(panel), (index * width, 28))
        draw.text((index * width + 5, 7), label, fill="black")
    sheet.save(path, quality=90)


def _fit_reference(reference: np.ndarray, width: int, height: int) -> np.ndarray:
    image = Image.fromarray(reference)
    return np.asarray(ImageOps.fit(image, (width, height), method=Image.Resampling.LANCZOS))


if __name__ == "__main__":
    main()
