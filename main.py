#!/usr/bin/env python3

import utils
from downloader import Downloader
from logger import PublicLogger
from files_to_download import *


def download_history(past_days, logger):
    downloader = Downloader(logger)

    yesterday_id = utils.get_previous_working_day_date_id()
    for date_id in range(yesterday_id - past_days + 1, yesterday_id + 1):
        for file_type in files_to_download:
            downloader.download(
                files_to_download[file_type].format(date_id),
                date_id
            )


if __name__ == '__main__':
    logger = PublicLogger()
    download_history(3, logger)
