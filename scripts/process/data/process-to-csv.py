import gzip
import json
import csv
import os
import zlib
from transactions.constants import DATA_PATH, RESULTS_PATH

def process_file_to_csv(filename, write_header):
    output_file = os.path.join(DATA_PATH, "data_ct_1y", "transactions-data_ct_1y.csv")
    try:
        with gzip.open(os.path.join(DATA_PATH, "data_ct_1y", filename), "rt") as file:
            with open(output_file, 'a') as out_csv:  
                writer = None
                try:
                    for line in file:
                        try:
                            record = json.loads(line)
                            if writer is None:
                                writer = csv.DictWriter(out_csv, fieldnames=record.keys())
                                if write_header:
                                    writer.writeheader()
                            writer.writerow(record)
                        except json.JSONDecodeError as e:
                            print(f"JSON Decode Error in file {filename}: {e}")
                except EOFError:
                    print(f"Error: Compressed file {filename} ended unexpectedly.")
    except zlib.error as e:
        print(f"Decompression error in file {filename}: {e}")


if __name__ == '__main__':
    dir = os.path.join(DATA_PATH, "data_ct_1y")
    file_list = [f for f in os.listdir(dir) if f.endswith(".jsonl.gz")]
    write_header = True
    for file in file_list:
        process_file_to_csv(file, write_header)
        write_header = False
