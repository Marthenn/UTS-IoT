import os
import argparse
from PIL import Image
import glob

# Configuration
IMAGE_FOLDER = "./images"
OUTPUT_HEADER = "images.h"
RESIZE_WIDTH = 640
RESIZE_HEIGHT = 480

def image_to_array(image_path, varname, resize=False):
    with Image.open(image_path) as img:
        img = img.convert("RGB")

        if resize:
            img = img.resize((RESIZE_WIDTH, RESIZE_HEIGHT), Image.Resampling.LANCZOS)
            img.save(image_path, format="JPEG")

        from io import BytesIO
        buffer = BytesIO()
        img.save(buffer, format="JPEG")
        byte_data = buffer.getvalue()

    array_data = ""
    for i, b in enumerate(byte_data):
        array_data += f"0x{b:02x}, "
        if (i + 1) % 12 == 0:
            array_data += "\n"

    return f"const unsigned char {varname}[] PROGMEM = {{\n{array_data}\n}};\nconst unsigned int {varname}_len = {len(byte_data)};\n\n"

def main():
    parser = argparse.ArgumentParser(description="Convert images to C arrays.")
    parser.add_argument("--resize", action="store_true", help="Enable resizing of images.")
    parser.add_argument("--width", type=int, default=RESIZE_WIDTH, help="Resize width (default: 640).")
    parser.add_argument("--height", type=int, default=RESIZE_HEIGHT, help="Resize height (default: 480).")
    args = parser.parse_args()

    header_content = "// AUTO-GENERATED IMAGE HEADER FILE\n\n#pragma once\n#include <pgmspace.h>\n\n"

    image_files = glob.glob(os.path.join(IMAGE_FOLDER, "*.*"))
    supported_ext = [".jpg", ".jpeg", ".png", ".bmp"]

    count = 0
    for img_path in image_files:
        if not any(img_path.lower().endswith(ext) for ext in supported_ext):
            continue

        basename = os.path.basename(img_path)
        varname = os.path.splitext(basename)[0].replace(" ", "_").replace("-", "_")

        print(f"Processing {basename} → {varname}")
        header_content += image_to_array(img_path, varname, resize=args.resize)
        count += 1

    with open(OUTPUT_HEADER, "w") as f:
        f.write(header_content)

    print(f"✅ Generated '{OUTPUT_HEADER}' with {count} images.")

if __name__ == "__main__":
    main()
