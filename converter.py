import sys
from pathlib import Path
from PIL import Image, ImageEnhance

# 6-Color Palette for E Ink Spectra 6 (E6)
SPECTRA_6_PALETTE = [
    0, 0, 0,       # Black
    255, 255, 255, # White
    255, 0, 0,     # Red
    0, 255, 0,     # Green
    0, 0, 255,     # Blue
    255, 255, 0,   # Yellow
]

def adjust_for_epaper(img, brightness=1.2, contrast=1.25, saturation=1.3):
    """
    Pre-processes image to boost contrast, brightness, and color saturation
    so it doesn't look washed out or muddy on e-Paper.
    """
    # 1. Boost Brightness
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(brightness)
    
    # 2. Boost Contrast (helps push light tones to white and dark tones to black)
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    
    # 3. Boost Saturation (helps map colors to the vivid primary particles)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(saturation)
    
    return img

def convert_for_spectra6(input_path, output_path, target_size=(600, 400)):
    input_file = Path(input_path)
    output_file = Path(output_path)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 1. Load source image and convert to RGB
    img = Image.open(input_file).convert("RGB")

    # 2. Resize to panel resolution
    img = img.resize(target_size, Image.Resampling.LANCZOS)

    # 3. Apply color enhancements for e-Paper compensation
    img = adjust_for_epaper(img, brightness=1.2, contrast=1.25, saturation=1.3)

    # 4. Build palette definition image
    palette_data = SPECTRA_6_PALETTE + [0] * (768 - len(SPECTRA_6_PALETTE))
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette(palette_data)

    # 5. Quantize using Floyd-Steinberg dithering
    dithered_img = img.quantize(palette=palette_img, dither=Image.Dither.FLOYDSTEINBERG)

    # 6. Save as 24-bit RGB BMP
    final_img = dithered_img.convert("RGB")
    final_img.save(output_file, "BMP")
    print(f"Converted '{input_file}' -> '{output_file}' (Adjusted & Dithered)")

def batch_convert(raw_dir=r"Image_Draw\raw_images", pic_dir=r"Image_Draw\pic"):
    raw_path = Path(raw_dir)
    pic_path = Path(pic_dir)

    if not raw_path.exists():
        print(f"Directory not found: {raw_path}")
        return

    image_extensions = ("*.jpg", "*.jpeg", "*.png", "*.bmp", "*.webp")
    image_files = []
    for ext in image_extensions:
        image_files.extend(raw_path.glob(ext))
        image_files.extend(raw_path.glob(ext.upper()))

    if not image_files:
        print(f"No images found in {raw_path}")
        return

    for img_file in image_files:
        output_file = pic_path / f"{img_file.stem}.bmp"
        convert_for_spectra6(img_file, output_file)

if __name__ == "__main__":
    batch_convert()