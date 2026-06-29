import os
import shutil

def copy_assets():
    src_dir = os.path.dirname(os.path.abspath(__file__))
    dest_dir = os.path.join(src_dir, "static", "images")
    os.makedirs(dest_dir, exist_ok=True)
    
    mapping = {
        "hexochems logo.png": "hexochems_logo.png",
        "carbo.png": "liquid_container.png",
        "distinct-brick-column-design-base-contrasts-skeletal-concrete-upper-floors-revealing-phased-construction-material-layering-399930866.webp": "about_hero.webp",
        "distinct-brick-column-design-base-contrasts-skeletal-concrete-upper-floors-revealing-phased-construction-material-layering-399930870.webp": "construction_site.webp",
        "rcc-frame-structure-services-500x500.webp": "powder_bag.webp",
        "column-sizes-for-commercial-building.webp": "column_design.webp",
        "venwiz-PCC-RCC.jpg": "pcc_rcc.jpg"
    }
    
    print("Copying assets to static/images...")
    for src_name, dest_name in mapping.items():
        src_path = os.path.join(src_dir, src_name)
        dest_path = os.path.join(dest_dir, dest_name)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied: {src_name} -> {dest_name}")
        else:
            print(f"File not found: {src_path}")
            
    print("Asset copy completed.")

if __name__ == "__main__":
    copy_assets()
