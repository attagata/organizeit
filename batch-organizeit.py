# 2023/08/03 v1.0.0 new helper batch-organizeit.py allows to run organizeit separated with diff main folders
#  USAGE: python3 batch-organizeit.py /Volumes/XYZ/Albums --dont_keep_running_at_end --skip-filename-with-exif --delete-temp-files --delete-source

import os
import subprocess
import argparse
import re

def normalize_folder_name(name):
    # Remove any special characters and replace spaces with "_"
    normalized_name = re.sub(r"[^a-zA-Z0-9_]", "", name.replace(" ", "_"))

    # Capitalize the first letter of each word
    normalized_name = " ".join(word.capitalize() for word in normalized_name.split("_"))

    return normalized_name.replace(" ", "_")

def create_destination_folder(source_folder, subfolder):
    # Normalize the subfolder name by removing spaces and special characters
    normalized_subfolder = normalize_folder_name(subfolder)

    # Create the destination folder by appending the normalized name to the source folder
    return os.path.join(source_folder, "../_OK", normalized_subfolder + "-OK")

def run_organize_it(src_dir, dst_dir, skip_exif=False, delete_temp=False, dont_keep_running_at_end=False, delete_source=False, text_append=None):
    # Construct the command to run the organize_it.py script
    cmd = [
        "python3",
        "organizeit.py",
        "--src_dir",
        src_dir,
        "--dst_dir",
        dst_dir
    ]

    # Add optional parameters if specified
    if skip_exif:
        cmd.append("--skip-filename-with-exif")
    if delete_temp:
        cmd.append("--delete-temp-files")
    if dont_keep_running_at_end:
        cmd.append("--dont_keep_running_at_end")
    if delete_source:
        cmd.append("--delete-source")
    if text_append:
        cmd.append("--append_to_filename")
        cmd.append(text_append)
            
    print(cmd)

    # Run the organize_it.py script with the given parameters
    subprocess.run(cmd)

def main():
    parser = argparse.ArgumentParser(description="Script to organize subfolders")
    parser.add_argument("source_folder", help="Main source folder")
    parser.add_argument("--skip-filename-with-exif", action="store_true", help="Skip filenames with EXIF data")
    parser.add_argument("--delete-temp-files", action="store_true", help="Delete temporary files")
    parser.add_argument("--dont_keep_running_at_end", action="store_true", help="Stops run when reaches the end.")
    parser.add_argument("--delete-source", action="store_true", default=False, help="Delete the source file after moving it to the destination directory.")
    args = parser.parse_args()

    source_folder = args.source_folder
    skip_exif = args.skip_filename_with_exif
    delete_temp = args.delete_temp_files
    dont_keep_running_at_end = args.dont_keep_running_at_end
    delete_source = args.delete_source

    # Iterate through subfolders and run the organize_it.py script for each one
    for subfolder in os.listdir(source_folder):
        subfolder_path = os.path.join(source_folder, subfolder)
        if os.path.isdir(subfolder_path):
            destination_folder = create_destination_folder(source_folder, subfolder)
            destination_folder_path = os.path.join(source_folder, destination_folder)
            
            # Call run_organize_it with --append_to_filename set to the subfolder name
            run_organize_it(subfolder_path, destination_folder_path, skip_exif, delete_temp, dont_keep_running_at_end, delete_source, text_append="_"+normalize_folder_name(subfolder))

if __name__ == "__main__":
    main()
