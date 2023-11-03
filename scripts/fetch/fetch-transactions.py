from datetime import datetime
from functools import partial
from glob import glob
import multiprocessing
import logging
import re
from os import path, rename

from transactions.constants import DATA_PATH
from transactions.utils import fetch_save_data, save_data

logging.basicConfig(level=logging.INFO)


break_points = [
    datetime(2023, 1, 1),
    datetime(2023, 4, 1),
    datetime(2023, 7, 1),
    datetime(2023, 10, 1)
]


gt_lt_list = [
    [break_points[i].timestamp(), break_points[i + 1].timestamp()]
    for i in range(0, len(break_points) - 1)
]

if __name__ == "__main__":
    pool = multiprocessing.Pool()
    pool.map(
        func=partial(
            fetch_save_data,
            limit=100,
            file_name="transactions",
            q="transactions",
            suburl="api/v1",
            rooturl="https://mainnet-public.mirrornode.hedera.com",
            number_iterations=1_000,
            counter_field_url="timestamp",
        ),
        iterable=gt_lt_list,
    )
