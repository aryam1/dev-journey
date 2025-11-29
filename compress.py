#!/usr/bin/env python3
import fitz
import argparse
import os

def compress_pdf(input_path, dpi=300):
    temp_path = input_path.replace(".pdf", "_temp.pdf")
    doc = fitz.open(input_path)
    new_doc = fitz.open()
    
    for page in doc:
        pix = page.get_pixmap(dpi=dpi)
        rect = page.rect
        new_page = new_doc.new_page(width=rect.width, height=rect.height)
        new_page.insert_image(rect, pixmap=pix)
    
    # Overwrite the input PDF with compressed version
    new_doc.save(temp_path, garbage=4, deflate=True, clean=True, incremental=False)
    new_doc.close()
    doc.close()
    
    os.remove(input_path)
    os.rename(temp_path, input_path)

def main():
    parser = argparse.ArgumentParser(description="Flatten & compress a PDF by rasterizing its pages.")
    parser.add_argument("pdf", help="Path to the PDF file to compress")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for rasterization (default: 300)")
    args = parser.parse_args()

    if not os.path.exists(args.pdf):
        print(f"Error: File {args.pdf} does not exist.")
        return

    print(f"Compressing {args.pdf} at {args.dpi} DPI...")
    compress_pdf(args.pdf, dpi=args.dpi)
    print("Done!")

if __name__ == "__main__":
    main()
