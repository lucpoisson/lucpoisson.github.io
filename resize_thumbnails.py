#!/usr/bin/env python3
"""
Script to resize all PNG thumbnails in assets/img/ to uniform dimensions
while maintaining aspect ratio and adding padding if needed.
"""

from PIL import Image, ImageOps
import os
import glob

# Configuration
THUMBNAIL_SIZE = (360, 280)  # Width x Height (2x CSS size for retina: 180x140)
BACKGROUND_COLOR = (248, 249, 250)  # Light gray background
INPUT_DIR = "assets/img"
OUTPUT_DIR = "assets/img/resized"

def resize_thumbnail(input_path, output_path, size=THUMBNAIL_SIZE, bg_color=BACKGROUND_COLOR):
    """
    Resize image to uniform dimensions with smart cropping/padding
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Calculate dimensions to fit within target size
            img.thumbnail(size, Image.Resampling.LANCZOS)
            
            # Create background with target size
            background = Image.new('RGB', size, bg_color)
            
            # Center the resized image on the background
            x = (size[0] - img.width) // 2
            y = (size[1] - img.height) // 2
            background.paste(img, (x, y))
            
            # Save with optimization
            background.save(output_path, 'PNG', optimize=True, quality=95)
            print(f"✅ Resized: {os.path.basename(input_path)}")
            
    except Exception as e:
        print(f"❌ Error processing {input_path}: {e}")

def main():
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Find all PNG files in assets/img (excluding subdirs)
    png_files = glob.glob(os.path.join(INPUT_DIR, "*.png"))
    
    if not png_files:
        print("No PNG files found in assets/img/")
        return
    
    print(f"Found {len(png_files)} PNG files to resize...")
    print(f"Target size: {THUMBNAIL_SIZE[0]}x{THUMBNAIL_SIZE[1]} pixels")
    print(f"Output directory: {OUTPUT_DIR}")
    print("-" * 50)
    
    for png_file in png_files:
        filename = os.path.basename(png_file)
        output_path = os.path.join(OUTPUT_DIR, filename)
        resize_thumbnail(png_file, output_path)
    
    print("-" * 50)
    print(f"✨ Completed! Resized {len(png_files)} thumbnails")
    print(f"📁 Check the resized images in: {OUTPUT_DIR}")
    print("\n🔄 To use the resized images:")
    print("1. Review the resized images in assets/img/resized/")
    print("2. If satisfied, replace the originals:")
    print("   cp assets/img/resized/*.png assets/img/")
    print("3. Delete the temp folder: rm -rf assets/img/resized/")

if __name__ == "__main__":
    main()
