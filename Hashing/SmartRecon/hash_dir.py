import os
import argparse

from nilsimsa import Nilsimsa


def main():
    parser = argparse.ArgumentParser(
        description="Convert pcapng files to feature vector representation with Nilsimsa. Hexidecimal digits output from Nilsimsa are converted to base10/decimal."
    )
    parser.add_argument(
        "inbase",
        type=str,
        help="Path to original files to be cleaned. Directory should be organized like inbase/files.",
    )
    parser.add_argument(
        "outbase",
        type=str,
        help="Path to save cleaned files.",
    )
    args = parser.parse_args()

    base = args.inbase

    hashes = []
    for folder in os.listdir(base):
        for file in os.listdir(base + folder):
            with open(base + folder + "/" + file, "rb") as file_obj:

                str1 = file_obj.read()

                n1 = Nilsimsa()
                n1.update(str1)

                hashed = n1.hexdigest()

                hashlist = []

                for x in range(0, len(hashed) - 1, 2):
                    hexdigit = str(hashed[x : x + 2])
                    dec = int(hexdigit, 16)
                    hashlist.append(str(dec))

                hashlist.append(folder)
                hashes.append(hashlist)

    with open(args.outbase, "w") as outfile:
        for item in hashes:
            outfile.write(",".join(item) + "\n")


if __name__ == "__main__":
    main()
