# Organize It (Python 3)

**Author:** Anderson Tagata  
**Version:** 1.3.3
**Release Date:** 2023/08/03

## Overview

**Organize It** is a Python 3 script designed to help you organize files in a source directory based on their EXIF or QuickTime metadata date. The script moves files to a destination directory, creating a folder structure based on the date and file extension. It also provides options to skip files with certain filenames, delete temporary files, and handle files with the same name by appending a sequence number.

## Features

- Extracts creation dates from EXIF or QuickTime metadata in image files.
- Organizes files into a destination directory based on the date and file extension.
- Skips files with certain filenames (e.g., containing "exif") using the `--skip-filename-with-exif` option.
- Deletes temporary files (e.g., .DS_Store, Thumbs.db) using the `--delete-temp-files` option.
- Forces to remove the source files using the `--delete-source` option.
- Handles files with the same name by appending a sequence number.

## Requirements

- Python 3
- `exiftool` library for extracting metadata from image files. Install it using the following command:
pip install exiftool


## Usage

1. Clone the repository or download the `organize_it.py` script.

2. Open a terminal or command prompt and navigate to the directory containing the `organize_it.py` script.

3. Run the script with the following arguments:

python organize_it.py --src_dir SOURCE_DIRECTORY --dst_dir DESTINATION_DIRECTORY [--skip-filename-with-exif] [--delete-temp-files]

**Arguments:**
- `--src_dir`: Path to the source directory. (Required)
- `--dst_dir`: Path to the destination directory. (Required)
- `--skip-filename-with-exif`: Optional. If set to True, the script skips files containing "exif" in the filename.
- `--delete-temp-files`: Optional. If set to True, the script deletes temporary files (e.g., .DS_Store, Thumbs.db).
- `--delete-source`: Optional. If set to True, the source file will be moved to the destination directory.

4. The script will continuously run in an infinite loop, reorganizing files in the source directory every 5 minutes.

## Example

python organize_it.py --src_dir /path/to/source --dst_dir /path/to/destination --skip-filename-with-exif --delete-temp-files --delete-source


5. Batch Helper

2023/08/03 v1.0.0 new helper batch-organizeit.py allows to run organizeit separated with diff main folders

USAGE: python3 batch-organizeit.py /Volumes/XYZ/Albums [--dont_keep_running_at_end] [--skip-filename-with-exif] [--delete-temp-files] [--delete-source]


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

Special thanks to the `exiftool` library creators for providing a powerful tool to extract metadata from image files.
