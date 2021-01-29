#!/usr/bin/env python3

from downloader import Downloader
from logger import PublicLogger


if __name__ == '__main__':
    logger = PublicLogger()

    downloader = Downloader(logger)
    downloader.download(
        'https://links.sgx.com/1.0.0/derivatives-historical/4821/WEBPXTICK_DT.zip',
        'WEBPXTICK_DT-20210127_PRO.zip'
    )
