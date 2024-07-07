#!/bin/bash

# Check if required commands are available
if ! command -v tar &> /dev/null || ! command -v pigz &> /dev/null; then
    echo "Error: This script requires 'tar' and 'pigz' to be installed."
    exit 1
fi

# Function to display usage information
usage() {
    echo "Usage: $0 -t <threads> -o <output_file> <directory1> [<directory2> ...]"
    echo "  -t <threads>    Number of threads to use for compression"
    echo "  -o <output_file>    Name of the output .tar.gz file"
    echo "  <directory1> [<directory2> ...]    Directories to compress"
    exit 1
}

# Parse command line arguments
threads=""
output_file=""
directories=()

while getopts "t:o:" opt; do
    case $opt in
        t) threads=$OPTARG ;;
        o) output_file=$OPTARG ;;
        *) usage ;;
    esac
done

shift $((OPTIND - 1))

# Check if required arguments are provided
if [ -z "$threads" ] || [ -z "$output_file" ] || [ $# -eq 0 ]; then
    usage
fi

# Add directories to the array
for dir in "$@"; do
    if [ -d "$dir" ]; then
        directories+=("$dir")
    else
        echo "Warning: '$dir' is not a directory. Skipping."
    fi
done

# Check if we have any valid directories
if [ ${#directories[@]} -eq 0 ]; then
    echo "Error: No valid directories specified."
    exit 1
fi

# Perform compression
echo "Compressing files from specified directories..."
tar cf - "${directories[@]}" | pigz -p "$threads" > "$output_file"

# Check if compression was successful
if [ $? -eq 0 ]; then
    echo "Compression complete. Output file: $output_file"
else
    echo "Error: Compression failed."
    exit 1
fi
