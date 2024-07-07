# Multi-threaded Compression and Decompression Scripts

This repository contains two Bash scripts for multi-threaded compression and decompression of files using tar and pigz.

## Requirements

- Bash shell
- tar
- pigz

## Compression Script (compress.sh)

This script compresses files from user-specified directories into a single .tar.gz file using a user-specified number of threads.

Usage:
./multithread_compress.sh -t <threads> -o <output_file> <directory1> [<directory2> ...]

- `-t <threads>`: Number of threads to use for compression
- `-o <output_file>`: Name of the output .tar.gz file
- `<directory1> [<directory2> ...]`: Directories to compress

Example:
./multithread_compress.sh -t 4 -o output.tar.gz /path/to/dir1 /path/to/dir2 /path/to/dir3

This example uses 4 threads to compress files from three directories into `output.tar.gz`.

## Decompression Script (decompress.sh)

This script decompresses a .tar.gz file created by the compression script, using a user-specified number of threads.

Usage:
./multithread_decompress.sh -t <threads> -i <input_file> -o <output_directory>

- `-t <threads>`: Number of threads to use for decompression
- `-i <input_file>`: Name of the input .tar.gz file
- `-o <output_directory>`: Directory to extract files to

Example:
./multithread_decompress.sh -t 4 -i output.tar.gz -o /path/to/extract

This example uses 4 threads to decompress `output.tar.gz` into the `/path/to/extract` directory.

## Notes

- Both scripts require `tar` and `pigz` to be installed on your system.
- The compression script will skip any specified paths that are not directories.
- The decompression script will create the output directory if it doesn't exist.
- Both scripts will display usage information if run without the required arguments.

## Error Handling

Both scripts include basic error handling:
- They check for the presence of required commands (tar and pigz).
- They validate the input arguments.
- They check if the compression/decompression process was successful.

If any errors occur, the scripts will display an appropriate error message and exit with a non-zero status code.
