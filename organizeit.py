# Anderson Tagata
# Organize it (Python 3)
# 2023/07/27

import os
import shutil
import filecmp
import time
from datetime import datetime
import argparse

# Create the parser and add arguments
parser = argparse.ArgumentParser()
parser.add_argument('--src_dir', required=True, help='Path to the source directory')
parser.add_argument('--dst_dir', required=True, help='Path to the destination directory')
args = parser.parse_args()

# Extract source and destination directories from the parsed arguments
src_dir = args.src_dir
dst_dir = args.dst_dir
ignored_dir = os.path.join(dst_dir, 'IGNORED')

# Create IGNORED directory if it doesn't exist
try:
    if not os.path.exists(ignored_dir):
        os.makedirs(ignored_dir)
except Exception as e:
    print(f"Error creating directory {ignored_dir}: {e}")

# Create a dictionary to track sequence numbers for each filename
sequence_dict = {}

# Initialize counters
moved_files = 0
ignored_files = 0

# Function to recursively remove empty directories
def remove_empty_dirs(dir):
    for dirpath, dirnames, filenames in os.walk(dir, topdown=False):
        if not os.listdir(dirpath):
            try:
                os.rmdir(dirpath)
                print(f"{datetime.now().replace(microsecond=0)} - Removed empty directory: {dirpath}")
            except Exception as e:
                print(f"Error removing directory {dirpath}: {e}")

while True:
    # Walk through the source directory recursively
    for dirpath, dirnames, filenames in os.walk(src_dir):
        # Iterate through each file in the current directory
        for filename in filenames:
            # Get the full path of the file
            file = os.path.join(dirpath, filename)

            # Check if the path is a file
            if os.path.isfile(file):
                # Get the modification time and convert it to a datetime object
                timestamp = os.path.getmtime(file)
                dt_obj = datetime.fromtimestamp(timestamp)

                # Format the datetime object to 'yyyymmdd' string
                year_month_day = dt_obj.strftime('%Y%m%d')
                # Format the datetime object to 'hhmmss' string
                time_format = dt_obj.strftime('%H%M%S')

                # Get the file extension and convert it to uppercase
                extension = os.path.splitext(file)[1].upper().replace(".", "")

                # Construct the new directory path
                new_dir = os.path.join(dst_dir, extension, year_month_day[:6], year_month_day)  # added another subfolder level for the day

                # Check if the new directory exists, if not then create it
                try:
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)
                except Exception as e:
                    print(f"Error creating directory {new_dir}: {e}")

                # Construct the new filename without the sequence number
                new_filename_without_seq = f"{year_month_day}_{time_format}"

                # Construct the full new filename without the sequence number
                new_filename = f"{new_filename_without_seq}.{extension.lower()}"
                # Construct the new file path
                new_file_path = os.path.join(new_dir, new_filename)

                # Check if a file with the same name exists in the new directory
                if os.path.exists(new_file_path):
                    # If the contents of the files are the same, move it to the ignored directory
                    try:
                        if filecmp.cmp(file, new_file_path, shallow=True):
                            print(f"{datetime.now().replace(microsecond=0)} - Ignoring duplicate file: {filename}")
                            shutil.move(file, os.path.join(ignored_dir, filename))
                            ignored_files += 1
                            continue
                    except Exception as e:
                        print(f"Error comparing or moving file {file} to {ignored_dir}: {e}")
                        
                    else:  # If the contents differ, increment the sequence and rename
                        if new_filename_without_seq in sequence_dict:
                            sequence = sequence_dict[new_filename_without_seq]
                        else:
                            sequence = 0
                        new_filename = f"{new_filename_without_seq}_{str(sequence).zfill(3)}.{extension.lower()}"
                        new_file_path = os.path.join(new_dir, new_filename)
                        sequence_dict[new_filename_without_seq] = sequence + 1

                # Calculate file size in MB
                file_size_MB = os.path.getsize(file) / (1024 * 1024) # in Megabytes
                print(f"{datetime.now().replace(microsecond=0)} - Moving: {filename} >> {new_file_path} - {file_size_MB:.2f} MB")

                # Move the file to the new directory
                try:
                    shutil.move(file, new_file_path)
                    moved_files += 1
                except Exception as e:
                    print(f"Error moving file {file} to {new_file_path}: {e}")

    # Remove empty directories
    remove_empty_dirs(src_dir)

    print(f"{datetime.now().replace(microsecond=0)} - Total moved files: {moved_files}")
    print(f"{datetime.now().replace(microsecond=0)} - Total ignored files: {ignored_files}")

    # Wait for 5 minutes before the next iteration
    time.sleep(300)
