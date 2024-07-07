#!/bin/bash

# Check if required commands are available
if ! command -v tar &> /dev/null || ! command -v pigz &> /dev/null; then
    echo "Error: This script requires 'tar' and 'pigz' to be installed."
    exit 1
fi

# Function to display usage information
usage() {
    echo "Usage: $0 -t <threads> -i <input_file> -o <output_directory>"
    echo "  -t <threads>    Number of threads to use for decompression"
    echo "  -i <input_file>    Name of the input .tar.gz file"
    echo "  -o <output_directory>    Directory to extract files to"
    exit 1
}

# Parse command line arguments
threads=""
input_file=""
output_directory=""

while getopts "t:i:o:" opt; do
    case $opt in
        t) threads=$OPTARG ;;
        i) input_file=$OPTARG ;;
        o) output_directory=$OPTARG ;;
        *) usage ;;
    esac
done

# Check if required arguments are provided
if [ -z "$threads" ] || [ -z "$input_file" ] || [ -z "$output_directory" ]; then
    usage
fi

# Check if input file exists
if [ ! -f "$input_file" ]; then
    echo "Error: Input file '$input_file' does not exist."
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$output_directory"

# Perform decompression
echo "Decompressing $input_file..."
pigz -dc -p "$threads" "$input_file" | tar xf - -C "$output_directory"

# Check if decompression was successful
if [ $? -eq 0 ]; then
    echo "Decompression complete. Files extracted to: $output_directory"
else
    echo "Error: Decompression failed."
    exit 1
fi
