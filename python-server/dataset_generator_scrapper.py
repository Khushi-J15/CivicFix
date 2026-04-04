# 1) Install dependencies
# -----------------------
# icrawler: for image crawling
# pillow:   for image loading & processing
# pandas:   for CSV creation
# %pip install icrawler pillow pandas

# 2) Imports
# ----------
import os
from icrawler.builtin import BingImageCrawler
from PIL import Image
import pandas as pd
import shutil  

# 3) Configuration
# ----------------
# Mapping of civic issue categories to specific search queries
category_queries = {
    "Road": [
        "roads with potholes",
        "damaged roads",
        "broken streets"
    ],
    "Garden": [
        "falled tree on indian roads",
        "unclean garden areas",
        "damaged park benches"
    ],
    "Electricity": [
        "fallen electric poles",
        "exposed electric wires",
        "streetlight not working"
    ],
    "Drainage": [
        "open drainage roadside india",
        "clogged sewer on roads in india",
        "overflowing drainage in india"
    ],
    "Health & Hygiene": [
        "garbage on streets in india",
        "dirty public toilets in india",
        "unsanitary conditions in india"
    ],
    "Water": [
        "water pipe leakage in india",
        "open water valve in india",
        "water logging in india"
    ],
    "Animals": [
        "stray dogs on road",
        "cattle blocking traffic",
        "stray animals in city"
    ]
}

# Number of images per query
MAX_PER_QUERY = 400

# Base directories
DOWNLOAD_DIR  = "/kaggle/working/images"            # raw downloads
OUTPUT_DIR    = "/kaggle/working/images_processed"  # resized 224×224
CSV_PATH      = "/kaggle/working/labels.csv"

# 4) Step 1: Crawl & download images
# ----------------------------------
def download_images_for_all():
    for category, queries in category_queries.items():
        cat_folder = os.path.join(DOWNLOAD_DIR, category.replace(" ", "_"))
        os.makedirs(cat_folder, exist_ok=True)
        
        for q in queries:
            q_folder = os.path.join(cat_folder, q.replace(" ", "_"))
            os.makedirs(q_folder, exist_ok=True)
            
            crawler = BingImageCrawler(storage={"root_dir": q_folder})
            crawler.crawl(keyword=q, max_num=MAX_PER_QUERY)
            print(f"✓ Downloaded {MAX_PER_QUERY} images for query '{q}'")

# 5) Step 2: Resize & crop to 224×224, build CSV entries
# ------------------------------------------------------
def process_and_label():
    records = []
    
    for root, _, files in os.walk(DOWNLOAD_DIR):
        # compute where to save processed image
        rel_root = os.path.relpath(root, DOWNLOAD_DIR)
        out_root = os.path.join(OUTPUT_DIR, rel_root)
        os.makedirs(out_root, exist_ok=True)
        
        # infer category from path (first folder)
        category = rel_root.split(os.sep)[0]
        
        for fname in files:
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue
            
            src = os.path.join(root, fname)
            dst = os.path.join(out_root, fname)
            
            # open, resize short side→256, then center-crop 224×224
            with Image.open(src) as img:
                img = img.convert("RGB")
                img.thumbnail((256, 256), Image.BILINEAR)
                w, h = img.size
                left = (w - 224) / 2
                top  = (h - 224) / 2
                img_c = img.crop((left, top, left + 224, top + 224))
                img_c.save(dst)
            
            rel_path = os.path.relpath(dst, os.path.dirname(CSV_PATH))
            records.append({
                "relative_path": rel_path.replace("\\", "/"),
                "category": category
            })
            print(f"Processed → {rel_path}")
    
    # write CSV
    df = pd.DataFrame(records)
    df.to_csv(CSV_PATH, index=False)
    print(f"\n✓ Labels CSV saved to {CSV_PATH} ({len(df)} entries)")

# 6) Main execution
# -----------------
if __name__ == "__main__":
    print("Starting downloads...")
    download_images_for_all()
    
    print("\nResizing & labeling...")
    process_and_label()
    
    # Cleanup: remove raw downloaded images
    if os.path.exists(DOWNLOAD_DIR):
        shutil.rmtree(DOWNLOAD_DIR)
        print(f"\n✓ Removed raw images directory: {DOWNLOAD_DIR}")
    
    print("\nAll done! You now have:")
    print(f" • Processed images: {OUTPUT_DIR}")
    print(f" • CSV labels:       {CSV_PATH}")
