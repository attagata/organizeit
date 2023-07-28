# organizeit
Helps you to reorganize files from a source folder by renaming and reallocate them in to folder organized structure based on date-time. Python.
Command need 2 parameters:
I suggest you to test with dummies files before to put it on real work time.

Usage:
python3 organizeit.py --src_dir /Volumes/NTFS05TB/SOURCE --dst_dir /Volumes/NTFS05TB/DESTINATION

'--src_dir' = 'Path to the source directory'

'--dst_dir' = 'Path to the destination directory'

It will move the files showing the source and destination and file size.

In case the file already exists on destination, it will move it to IGNORE subfolder of DESTINATION.

It will run and wait for 5 minutes to run it again, to force stop it, user CTRL+C.

Here is the table of features:

The script takes two arguments from the command line, --src_dir and --dst_dir, which are the source and destination directories for file management.

It creates an IGNORED directory under the destination directory. This directory seems to be used for storing duplicate files.

The script then enters a while True loop, essentially running indefinitely until manually stopped. Within this loop, it recursively traverses through all files in the source directory.

For each file in the source directory, it gets the modification time and constructs a new directory path in the destination directory based on the file's extension and modification date.

If a file with the same name already exists at the destination path, it checks if the contents of the two files are identical. If they are, it moves the file from the source directory to the IGNORED directory.

If the files are not identical, it adds a sequence number to the filename to avoid a naming collision and then moves the file to the new directory.

The script keeps a count of how many files it has moved and how many it has ignored (due to being duplicates).

Finally, it removes any empty directories in the source directory and prints out the total number of moved and ignored files before pausing for 5 minutes (300 seconds). After the pause, the loop starts again.
