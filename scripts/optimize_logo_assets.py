"""Generate responsive, cache-friendly logo variants from the source artwork.

The source logos stay untouched.  This script intentionally writes only the
small variants consumed by index.html, so regenerating them is deterministic
when the artwork or WebP encoder settings change.
"""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "images"


def write_webp(source_name: str, output_name: str, width: int, quality: int = 80) -> None:
    source_path = IMAGE_DIR / source_name
    output_path = IMAGE_DIR / output_name
    with Image.open(source_path) as source:
        source = source.convert("RGBA" if "A" in source.getbands() else "RGB")
        height = round(source.height * width / source.width)
        resized = source.resize((width, height), Image.Resampling.LANCZOS)
        resized.save(
            output_path,
            format="WEBP",
            quality=quality,
            method=6,
            lossless=False,
            exact=False,
        )
        print(f"{output_path.relative_to(ROOT)}: {width}x{height}")


def main() -> None:
    # Header banner: 1x and 2x candidates for its responsive intrinsic width.
    write_webp("logo-banner.webp", "logo-banner-480.webp", 480)
    write_webp("logo-banner.webp", "logo-banner-960.webp", 960)

    # Retain splash artwork variants for any non-blocking, post-load use.
    write_webp("logo-splash-new.webp", "logo-splash-new-320.webp", 320)
    write_webp("logo-splash-new.webp", "logo-splash-new-640.webp", 640)

    # Footer renders at 40 CSS pixels; these candidates avoid shipping 256px art.
    write_webp("logo.webp", "logo-footer-80.webp", 80)
    write_webp("logo.webp", "logo-footer-160.webp", 160)


if __name__ == "__main__":
    main()