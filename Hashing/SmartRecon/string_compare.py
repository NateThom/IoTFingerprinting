import sys
import os

from nilsimsa import Nilsimsa


def main():
    parser = argparse.ArgumentParser(
        description="Compute Nilsimsa similarity score of two files."
    )
    parser.add_argument(
        "string1",
        type=str,
        help="First string to be compared.",
    )
    parser.add_argument(
        "string2",
        type=str,
        help="Second string to be compared.",
    )
    args = parser.parse_args()

    str1 = args.string1
    str2 = args.string2

    n1 = Nilsimsa()
    n1.update(str1)

    n2 = Nilsimsa(str2)

    hash1 = n1.hexdigest()
    hash2 = n2.hexdigest()

    print(hash1)
    print(hash2)

    score = str(n1.compare(n2.digest()))
    print("Score: " + str(n1.compare(n2.digest())))


if __name__ == "__main__":
    main()
