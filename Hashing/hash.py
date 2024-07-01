import argparse
from multiprocessing import Pool

from flexhash import FlexHash
from nilsimsa import Nilsimsa


class Hash:
    def __init__(self, hash_alg="flexhash"):
        # init selected hashing object
        assert hash_alg in (
            "flexhash",
            "nilsimsa",
        ), f"'hash_alg' parameter must be either 'nilsimsa' or 'flexhash'"
        self.hash_alg = hash_alg
        if hash_alg == "flexhash":
            self.acc_size = input("Accumulator size [128, 256, 512, 1024]: ")
            self.window_size = input("Window size [4, 5, 6]: ")
            self.ngram_size = input(f"ngram size [2,...,{window_size}]: ")

    def hash_file(self, filename, label):
        with open(filename, "rb") as file_obj:
            file_contents = file_obj.read()
            if self.hash_alg == "flexhash":
                bytes_list = [byte_obj for byte_obj in file_contents]
                hash_obj = FlexHash(self.acc_size, self.window_size, self.ngram_size)
                output_hash = hash_obj.calc_digest(bytes_list, label)
            else:
                hash_obj = Nilsimsa()
                hash_obj.update(file_contents)
                output_hash = hash_obj.hexdigest()

                hash_list = []

                for x in range(0, len(output_hash) - 1, 2):
                    hexdigit = str(output_hash)
                    decimal = int(hexdigit, 16)
                    hashlist.append(str(decimal))

                hashlist.append(label)
                output_hash = hash_list
        return output_hash

    def hash_directory(
        self, input_path, output_path, out_file_type="parquet", n_jobs=1
    ):
        assert out_file_type in (
            "parquet",
            "csv",
        ), f"'out_file_type' parameter must be either 'parquet' or 'csv'"

        hash_file_inputs = []
        for folder in os.listdir(input_path):
            for file in os.listdir("/".join(input_path, folder)):
                hash_file_inputs.append("/".join(input_path, folder, file), folder)

        with Pool() as p:
            output = p.starmap(hash_file, hash_file_inputs)

        output_df = pd.DataFrame(output)
        if out_file_type == "parquet":
            output_df.to_parquet(f"{output_path}.parquet.gzip", compression="gzip")
        else:
            output_df.to_csv(f"{output_path}.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert pcapng files to feature vector representation with a hashing function. Hexidecimal digits output from Nilsimsa are converted to base10/decimal."
    )
    parser.add_argument(
        "inbase",
        type=str,
        help="Path to original files to be hashed. Directory should be organized like inbase/files.",
    )
    parser.add_argument(
        "outbase",
        type=str,
        help="Path to save dataset.",
    )
    parser.add_argument(
        "hash_alg",
        type=str,
        help="Should be either nilsimsa or flexhash.",
    )
    parser.add_argument(
        "out_file_type",
        type=str,
        default="parquet",
        help="Output file type. Either csv or parquet.",
    )
    args = parser.parse_args()

    hash_obj = Hash(hash_alg=args.hash_alg)
