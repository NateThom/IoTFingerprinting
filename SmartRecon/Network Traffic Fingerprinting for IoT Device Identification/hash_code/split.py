import os
import os.path
from itertools import combinations
import itertools
import random
import subprocess
import sys
import time

import numpy as np


def splitter(input_pcap, outputbase, increment):
    command = "tshark -r " + input_pcap + " -T fields -e frame.time_relative"
    proc = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    splitted = out.split(b"\n")
    last_second = int(float(splitted[-2]))


    window_insecond = 60 * 1
    counter = 1
    if last_second > window_insecond:
        for i in range(0, last_second, 60 * 1):

            start_time = i
            end_time = i + window_insecond
            output_pcap = (
                outputbase
                + input_pcap.split("/")[-1].split(".pcap")[0]
                + "-"
                + str(counter)
                + ".pcap"
            )

            command = "tshark -r " + input_pcap
            command += " -Y 'frame.time_relative >= "
            command += + str(start_time)
            command += + " and frame.time_relative <= "
            command += str(end_time) + "' -w "
            command += output_pcap

            os.system(command)

            if (end_time + 60 * 1) > last_second:
                break
            counter = counter + 1

    print("finished", input_pcap)


def main():
    parser = argparse.ArgumentParser(
        description="Split pcapng files into subfiles containing the packets which occur in a n-second time window."
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

    inpath = args.inbase
    outpath = args.outbase
    counter = 10

    for folder in os.listdir(inpath):
        for file in os.listdir(inpath + folder):
            input_pcap = inpath + folder + "/" + file
            outputbase = outpath + f"{counter}-minute/" + folder + "/"
            splitter(input_pcap, outputbase, counter)

if __name__ == "__main__":
    main()