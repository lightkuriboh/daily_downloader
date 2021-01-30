#!/usr/bin/env python3

import argparse
import datetime

import utils
from downloader import Downloader
from logger import PublicLogger
from files_to_download import files_to_download
from scheduler import JobScheduler
from recovery import retry_download


def init_parser():
    parser = argparse.ArgumentParser('This code was written by HieuPro!')
    parser.add_argument('-past_days', type=int, default=1,
                        help='The number of previous days you want to download (default = 1)')
    parser.add_argument('-hour', type=int, default=2,
                        help='Hour at which each day the job should be run (default = 2)')
    return parser.parse_args()


def download_history(past_days, logger):
    downloader = Downloader(logger)

    retry_download(downloader, past_days)

    yesterday_id = utils.get_previous_working_day_date_id()
    for date_id in range(max(1, yesterday_id - past_days + 1), yesterday_id + 1):
        for file_type in files_to_download:
            downloader.download(
                files_to_download[file_type].format(date_id),
                str(date_id)
            )


if __name__ == '__main__':
    args = init_parser()

    root_logger = PublicLogger()

    datetime_to_run = datetime.datetime.now().replace(hour=args.hour, minute=0)

    JobScheduler(datetime_to_run, download_history,
                 first_time_run_params={
                     'past_days': args.past_days,
                     'logger': root_logger
                 },
                 future_run_params={
                     'past_days': 1,
                     'logger': root_logger
                 }
    )
