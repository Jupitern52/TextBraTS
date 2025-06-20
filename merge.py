import os
import shutil

# === Please set your own paths below! ===
img_root = "/path/to/MICCAI_BraTS2020_TrainingData"
txt_root = "/path/to/Download/TextBraTSData"
out_root = "/path/to/TextBraTS/TextBraTSData"

# Loop over all cases in the image folder
for case in os.listdir(img_root):
    img_case_dir = os.path.join(img_root, case)
    txt_case_dir = os.path.join(txt_root, case)
    out_case_dir = os.path.join(out_root, case)

    if not os.path.isdir(img_case_dir):
        continue  # Skip non-directory files

    # Create output folder for each case
    os.makedirs(out_case_dir, exist_ok=True)

    # Copy all imaging files and segmentation labels
    for file in os.listdir(img_case_dir):
        shutil.copy2(os.path.join(img_case_dir, file), os.path.join(out_case_dir, file))

    # Copy text reports and feature files if available
    if os.path.exists(txt_case_dir):
        for file in os.listdir(txt_case_dir):
            shutil.copy2(os.path.join(txt_case_dir, file), os.path.join(out_case_dir, file))
    else:
        print(f"Warning: {txt_case_dir} does not exist, skipping.")

print("Merge done! All cases are in:", out_root)
