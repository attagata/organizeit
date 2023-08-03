# Anderson Tagata
# Organize it (Python 3)
# 2023/07/27 v1.0.0 first version
# 2023/07/28 v1.1.0 added exif read feature for EXIF:DateTimeOriginal
# 2023/07/29 v1.2.0 added exif read feature for QuickTime:CreationDate
# 2023/07/29 v1.3.0 added Skip Argument for files already named with exif
# 2023/07/29 v1.3.0 Remove only subfolders when is empty and keep the source folder
# 2023/08/01 v1.3.1 Files with error to get date, send them to ERROR subfolder
# 2023/08/01 v1.3.1 new arg --delete-temp-files to force delete of ocurrences .DS_Store or Thumbs.db

import os
import shutil
import filecmp
import time
from datetime import datetime
import argparse
import exiftool

# Create the parser and add arguments
parser = argparse.ArgumentParser()
parser.add_argument('--src_dir', required=True, help='Path to the source directory')
parser.add_argument('--dst_dir', required=True, help='Path to the destination directory')
parser.add_argument('--skip-filename-with-exif', default=False, action='store_true',
                    help='Skip files containing "exif" in the filename if set to True')
parser.add_argument('--delete-temp-files', default=False, action='store_true',
                    help='Delete temporary files (e.g., .DS_Store, Thumbs.db) if set to True')
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

# Function to get datetime from exif metadata
def get_exif_datetime(image_path):
    if not os.path.exists(image_path):
        print("Error: File not found.")
        return None

    # Use exiftool to get EXIF metadata from the image file
    with exiftool.ExifTool() as et:
        tags = et.execute_json('-EXIF:DateTimeOriginal', image_path)

    if tags and len(tags) > 0:
        # Extract the 'DateTimeOriginal' tag value from the EXIF metadata
        datetime_str = tags[0].get('EXIF:DateTimeOriginal')

        # Check if the datetime_str is not empty and not equal to '0000:00:00 00:00:00'
        if datetime_str and datetime_str.strip() and datetime_str != '0000:00:00 00:00:00':
            try:
                # Parse the datetime string to a datetime object
                return datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S')
            except ValueError:
                # If there is an error parsing the datetime, print an error message and return None
                print(f"Error parsing EXIF datetime for file {image_path}.")
                return None

    return None

# Function to get datetime from QuickTime metadata
def get_exif_datetime_quicktime(image_path):
    if not os.path.exists(image_path):
        print("Error: File not found.")
        return None

    # Use exiftool to get QuickTime metadata from the image file
    with exiftool.ExifTool() as et:
        tags = et.execute_json('-QuickTime:CreationDate', image_path)

    if tags and len(tags) > 0:
        # Extract the 'CreationDate' tag value from the QuickTime metadata
        datetime_str = tags[0].get('QuickTime:CreationDate')

        # Check if the datetime_str is not empty and not equal to '0000:00:00 00:00:00'
        if datetime_str and datetime_str.strip() and datetime_str != '0000:00:00 00:00:00':
            try:
                # Append ':00' to the timezone offset to make it in the format '+03:00'
                datetime_str += ':00'
                # Parse the datetime string to a datetime object with timezone information
                return datetime.strptime(datetime_str, '%Y:%m:%d %H:%M:%S%z')
            except ValueError:
                # If there is an error parsing the datetime, print an error message and return None
                print(f"Error parsing QuickTime datetime for file {image_path}.")
                return None

    return None

# Function to recursively remove empty directories
def remove_empty_dirs(dir):
    while True:
        # Initialize flag to False on each iteration
        dir_removed = False
        for dirpath, dirnames, filenames in os.walk(dir, topdown=False):
            # Check if the current directory is not the source directory and is empty
            if dirpath != dir and not any(dirnames) and not any(filenames):
                try:
                    os.rmdir(dirpath)
                    print(f"{datetime.now().replace(microsecond=0)} - Removed empty directory: {dirpath}")
                    # Set flag to True if a directory has been removed
                    dir_removed = True
                except Exception as e:
                    print(f"Error removing directory {dirpath}: {e}")
        
        # If no directories were removed in this iteration, break the loop
        if not dir_removed:
            break

while True:
    # Walk through the source directory recursively
    for dirpath, dirnames, filenames in os.walk(src_dir):
        # Iterate through each file in the current directory
        for filename in filenames:
            # Skip files with filenames ".DS_Store" or "Thumbs.db" if the --delete-temp-files argument is provided
            if args.delete_temp_files and (filename.lower() == ".ds_store" or filename.lower() == "thumbs.db"):
                try:
                    # Remove the file and continue with the next file
                    os.remove(os.path.join(dirpath, filename))
                    print(f"{datetime.now().replace(microsecond=0)} - Removed temporary file: {filename}")
                except Exception as e:
                    print(f"Error removing temporary file {filename}: {e}")
                continue

            # Get the full path of the file
            file = os.path.join(dirpath, filename)

            # Check if the file already exists in the IGNORED subfolder
            ignored_file_path = os.path.join(ignored_dir, filename)
            if os.path.isfile(ignored_file_path):
                try:
                    # Move it to IGNORED and continue with the next file
                    shutil.move(file, ignored_file_path)
                    ignored_files += 1
                    print(f"{datetime.now().replace(microsecond=0)} - Ignored: Moved {filename} to IGNORED.")
                    continue
                except Exception as e:
                    print(f"Error moving file {file} to {ignored_file_path}: {e}")

            # Check if the path is a file
            if os.path.isfile(file):
                # If --ignore-filename-with-exif is set to True and 'exif' is in the filename, skip this file
                if args.skip_filename_with_exif and 'exif' in filename.lower():
                    print(f"{datetime.now().replace(microsecond=0)} - Skipping file with 'exif' in filename: {filename}")
                    continue

                # Attempt to extract datetime from EXIF data
                dt_obj = get_exif_datetime(file)

                if dt_obj is None:
                    dt_obj = get_exif_datetime_quicktime(file)

                # If no EXIF data or unable to extract datetime, use file's modification time
                if dt_obj is None:
                    timestamp = os.path.getmtime(file)
                    dt_obj = datetime.fromtimestamp(timestamp)
                    sExif = ""
                else:
                    # Mark file with exif case date came from exif metatag
                    sExif = "_exif"

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
                new_filename = f"{new_filename_without_seq}{sExif}.{extension.lower()}"
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

