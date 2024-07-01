import os
import argparse

from nilsimsa import Nilsimsa


def main():
    parser = argparse.ArgumentParser(
        description="Compute Nilsimsa similarity score of two files."
    )
    parser.add_argument(
        "filepath1",
        type=str,
        help="Path to first file to be compared.",
    )
    parser.add_argument(
        "filepath2",
        type=str,
        help="Path to second file to be compared.",
    )
    args = parser.parse_args()

    file1 = args.filepath1
    file2 = args.filepath2

    with open(file1, "rb") as f1:
        with open(file2, "rb") as f2:

            file1 = f1.read()
            file2 = f2.read()

            n1 = Nilsimsa()
            n1.update(file1)

            n2 = Nilsimsa(file2)

            hash1 = n1.hexdigest()
            hash2 = n2.hexdigest()

            print(hash1)
            print(hash2)

            score = str(n1.compare(n2.digest()))
            print("Score: " + str(n1.compare(n2.digest())))


if __name__ == "__main__":
    main()
