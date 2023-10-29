import gzip
import json
import csv
import os
from transactions.constants import DATA_PATH, RESULTS_PATH

def process_file_to_csv(filename, write_header):
    output_file = os.path.join(DATA_PATH, "transactions-data-ct.csv")
    with gzip.open(os.path.join(DATA_PATH, filename), "rt") as file:
        with open(output_file, 'a') as out_csv:  
            writer = None
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

if __name__ == '__main__':
    file_list = [f for f in os.listdir(DATA_PATH) if f.endswith(".jsonl.gz")]
    write_header = True
    for file in file_list:
        process_file_to_csv(file, write_header)
        write_header = False
