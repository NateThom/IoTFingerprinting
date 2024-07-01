import sys
import os
import time
import argparse


def main():

    parser = argparse.ArgumentParser(
        description="Anonymize pcapng traffic by setting ip/mac address to 1s and recalculating checksums."
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
    parser.add_argument(
        "--sleep",
        default=0.0,
        type=float,
        help="Time to sleep between system calls. Only use this if system is behaving strangely during processing.",
    )
    args = parser.parse_args()

    hashes = []

    for file in os.listdir(inbase):
        inputfile = args.inbase + file
        outputfile = args.outbase + file

        command1 = (
            "tcprewrite --dlt=enet --infile="
            + inputfile
            + " "
            + "--outfile=temp.pcapng"
        )
        command2 = (
            "tcprewrite --enet-dmac=11:11:11:11:11:11 --enet-smac=11:11:11:11:11:11 --pnat=192.168.0.0/16:1.1.1.1/32 --infile=temp.pcapng --outfile="
            + outputfile
        )

        os.system(command1)
        time.sleep(args.sleep)

        os.system(command2)
        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
