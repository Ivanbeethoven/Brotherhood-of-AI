#!/usr/bin/env python3
"""
cover_and_extract.py

Usage:
    python3 cover_and_extract.py <input.pdf> <week_dir>

This script:
1. Renders the first page of the PDF as a PNG cover (150 DPI).
2. Extracts all embedded true-color (RGB) images from the PDF.
3. Generates a README.md showcasing the PDF and images in a nice table.

Dependencies:
    pip install PyMuPDF
"""

import sys
import os
import fitz  # PyMuPDF

def render_cover(doc, pdf_path, out_dir, dpi=150):
    page = doc[0]
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    base = os.path.splitext(os.path.basename(pdf_path))[0]
    cover_path = os.path.join(out_dir, f"{base}.png")
    pix.save(cover_path)
    print(f"✔ Saved cover image: {cover_path}")
    return cover_path

def extract_rgb_images(doc, pdf_path, out_dir, base_name):
    image_paths = []
    count = 0
    for page_index in range(len(doc)):
        images = doc[page_index].get_images(full=True)
        for img_info in images:
            xref = img_info[0]
            pix = fitz.Pixmap(doc, xref)
            if pix.n == 3:  # RGB only
                width, height = pix.width, pix.height
                out_file = os.path.join(
                    out_dir,
                    f"{base_name}_page{page_index+1}_img{xref}_w{width}_h{height}.png"
                )
                pix.save(out_file)
                image_paths.append((out_file, width * height))
                count += 1
            pix = None
    print(f"✔ Total RGB images extracted: {count}")
    return image_paths

def generate_readme(week_dir, pdf_path, cover_path, image_paths):
    base_pdf = os.path.basename(pdf_path)
    base_name = os.path.splitext(base_pdf)[0]
    readme_path = os.path.join(week_dir, "README.md")

    # 选最大尺寸图作为“核心插图”
    core_image = None
    if image_paths:
        core_image = sorted(image_paths, key=lambda x: x[1], reverse=True)[0][0]

    with open(readme_path, "w") as f:
        f.write(f"# 🗓️ Week {os.path.basename(week_dir)} 论文精选\n\n")
        f.write(f"## [{base_name}]({base_pdf})\n\n")
        f.write("<table><tr>\n")
        f.write(f'  <td><img src="./{os.path.basename(cover_path)}" alt="PDF 首页" width="500"/></td>\n')
        if core_image:
            f.write(f'  <td><img src="./{os.path.basename(core_image)}" alt="核心插图" width="500"/></td>\n')
        else:
            f.write('  <td><em>无核心插图可显示</em></td>\n')
        f.write("</tr></table>\n")
    print(f"✔ Generated README: {readme_path}")

def main():
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <input.pdf> <week_dir>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    week_dir = sys.argv[2]
    os.makedirs(week_dir, exist_ok=True)

    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    doc = fitz.open(pdf_path)

    cover_path = render_cover(doc, pdf_path, week_dir)
    image_paths = extract_rgb_images(doc, pdf_path, week_dir, base_name)
    generate_readme(week_dir, pdf_path, cover_path, image_paths)

if __name__ == "__main__":
    main()
