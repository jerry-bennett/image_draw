import numpy as np
import cv2
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

def generate_split_mask(height, width, orientation="diagonal", split_ratio=0.55):
    """
    Creates a smooth 0.0 to 1.0 mask dividing the clean image from the liquid glitch.
    Modes: 'vertical', 'horizontal', or 'diagonal'
    """
    grid_y, grid_x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')

    if orientation == "horizontal":
        boundary = height * split_ratio + np.sin(grid_x * 0.02) * 20
        raw_mask = grid_y - boundary
    elif orientation == "vertical":
        boundary = width * split_ratio + np.sin(grid_y * 0.02) * 20
        raw_mask = grid_x - boundary
    else:  # diagonal split
        diagonal_coord = grid_x * 0.7 + grid_y * 0.7
        boundary = (width * 0.7 + height * 0.7) * split_ratio + np.sin(grid_x * 0.015) * 25
        raw_mask = diagonal_coord - boundary

    # Sigmoid blend for a natural transition zone along the boundary
    mask = 1.0 / (1.0 + np.exp(-raw_mask / 15.0))
    return np.stack([mask] * 3, axis=-1)

def apply_visible_liquid_waves(np_img, wave_length=45, amplitude=30):
    h, w, c = np_img.shape
    grid_x, grid_y = np.meshgrid(np.arange(w), np.arange(h))

    k = 2 * np.pi / wave_length
    wave_x = np.sin(grid_y * k) * amplitude
    wave_y = np.cos(grid_x * k * 0.6) * (amplitude * 0.7)

    map_x = (grid_x + wave_x).astype(np.float32)
    map_y = (grid_y + wave_y).astype(np.float32)

    return cv2.remap(np_img, map_x, map_y, 
                     interpolation=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)

def apply_dark_drips(np_img, num_drips=6, min_width=10, max_width=28, min_len=100, max_len=260):
    h, w, c = np_img.shape
    out_img = np_img.copy()
    gray = cv2.cvtColor(np_img, cv2.COLOR_RGB2GRAY)
    
    dark_y, dark_x = np.where(gray < 160)
    if len(dark_x) == 0:
        dark_x = np.arange(10, w - 30)

    indices = np.random.choice(len(dark_x), size=min(num_drips, len(dark_x)), replace=False)

    for idx in indices:
        start_x = dark_x[idx]
        start_y = dark_y[idx] if len(dark_y) > idx else np.random.randint(10, int(h * 0.4))
        
        drip_w = np.random.randint(min_width, max_width)
        end_x = min(start_x + drip_w, w)
        
        drip_h = np.random.randint(min_len, max_len)
        end_y = min(start_y + drip_h, h)

        sample_color = (np_img[start_y, start_x:end_x].mean(axis=0) * 0.5).astype(np.uint8)
        
        for y in range(start_y, end_y):
            fade_factor = (y - start_y) / float(end_y - start_y)
            if fade_factor > 0.7:
                blend = max(0.0, (1.0 - fade_factor) / 0.3)
                color = (sample_color * blend).astype(np.uint8)
                out_img[y, start_x:end_x] = color
            else:
                out_img[y, start_x:end_x] = sample_color

    return out_img

def convert_for_spectra6(input_path, output_path, target_size=(600, 400), split_type="diagonal", split_ratio=0.5):
    input_file = Path(input_path)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 1. Load source image and resize
    pil_img = Image.open(input_file).convert("RGB")
    pil_img = pil_img.resize(target_size, Image.Resampling.LANCZOS)
    clean_np = np.array(pil_img)

    # 2. Build liquid/glitched variant
    warped_np = apply_visible_liquid_waves(clean_np, wave_length=45, amplitude=32)
    glitched_np = apply_dark_drips(warped_np, num_drips=6, min_width=10, max_width=26)

    # 3. Generate dynamic mask and blend clean + liquid sides
    mask = generate_split_mask(target_size[1], target_size[0], orientation=split_type, split_ratio=split_ratio)
    blended = (clean_np * (1.0 - mask) + glitched_np * mask).astype(np.uint8)

    # 4. Color & contrast adjustment
    art_img = Image.fromarray(blended)
    art_img = ImageEnhance.Brightness(art_img).enhance(1.1)
    art_img = ImageEnhance.Contrast(art_img).enhance(1.3)
    art_img = ImageEnhance.Color(art_img).enhance(1.35)

    # 5. Dither to Spectra 6 palette
    palette_data = SPECTRA_6_PALETTE + [0] * (768 - len(SPECTRA_6_PALETTE))
    palette_img = Image.new("P", (1, 1))
    palette_img.putpalette(palette_data)

    dithered_img = art_img.quantize(palette=palette_img, dither=Image.Dither.FLOYDSTEINBERG)

    # 6. Save BMP
    final_img = dithered_img.convert("RGB")
    final_img.save(output_file, "BMP")
    print(f"Generated Masked Liquid Glitch BMP: '{output_file}'")

if __name__ == "__main__":
    # Options for split_type: 'diagonal', 'vertical', or 'horizontal'
    # split_ratio: 0.3 to 0.7 adjusts where the split line cuts across the canvas
    convert_for_spectra6(r"raw_images\wlf.jpg", r"pic\subtle_glitch.bmp", split_type="diagonal", split_ratio=0.5)