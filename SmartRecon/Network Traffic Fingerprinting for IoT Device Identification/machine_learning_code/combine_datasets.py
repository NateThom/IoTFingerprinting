import os

import pandas as pd

def main():
    parser = argparse.ArgumentParser(
        description="Combine various device classes/csvs into a single file."
    )
    parser.add_argument(
        "n_dims",
        type=int,
        help="The number of dimensions/features in the files being cusomtized."
    )
    parser.add_argument(
        "input_path",
        type=str,
        help="Path to root of datasets to combine.",
    )
    args = parser.parse_args()

    col_names = [f"dim{i}" for i in range(1, args.n_dims+1)]
    col_names.append("class")

    path_to_dataset = args.input_path
    device_csvs = os.listdir(path_to_dataset)
    if "combined.csv" in device_csvs:
        device_csvs.remove("combined.csv")

    final_df = pd.DataFrame(columns=col_names)

    for index, csv_name in enumerate(device_csvs):
        temp_df = pd.read_csv(path_to_dataset + csv_name, names=col_names)

        final_df = pd.concat([final_df, temp_df])

    final_df.to_csv(path_to_datasets + "combined.csv", index=False)

if __name__ == "__main__":
    main()