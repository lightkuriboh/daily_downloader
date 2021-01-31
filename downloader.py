import shutil
import urllib3

import utils
from recovery import DownloadedFiles, RecoveryFiles, RecoveryInfo


class Downloader:
    DOWNLOAD_CONTENT_TYPES = ['application/octet-stream', 'application/download']
    DOWNLOAD_ROOT_DIR = 'downloaded'
    DOWNLOAD_TEMP_DIR = 'temp'

    def __init__(self, logger):
        self.logger = logger
        self.date_id_map = {}

        self.downloaded_files = DownloadedFiles.load_success_files()

    def get_file_info(self, file_url, connection):
        file_getter = connection.urlopen('HEAD', file_url)

        if file_getter.info()['Content-Type'] not in Downloader.DOWNLOAD_CONTENT_TYPES:
            self.logger.error('File not found: {}'.format(file_url))
            return None

        file_info = {
            'file_size': int(file_getter.info()['Content-Length']),
            'file_name': utils.get_file_name(file_getter.info()['Content-Disposition'])
        }
        return file_info['file_size'], file_info['file_name']

    def __get_destination_file(self, root_folder, file_name, date_id):
        inferred_date = utils.get_date_from_filename(file_name)
        destination_folder = self.date_id_map[date_id] if date_id in self.date_id_map else inferred_date
        if date_id not in self.date_id_map:
            self.date_id_map[date_id] = destination_folder

        directory = '/'.join([root_folder, destination_folder])
        utils.create_folder(directory)

        return '/'.join([directory,
                         file_name if file_name else destination_folder])

    def download(self, file_url, date_id):
        http = urllib3.PoolManager()
        file_infos = self.get_file_info(file_url, http)
        total_size, file_name = (0, '') if not file_infos else file_infos

        if total_size == 0:
            RecoveryFiles.add_failed_file(date_id, file_url)
            return
        if total_size > 1e9:
            self.logger.warn('Large file size: {}MB from url: {}'.format(total_size / 1e6, file_url))

        destination_file_path = self.__get_destination_file(Downloader.DOWNLOAD_TEMP_DIR, file_name, date_id)
        final_destination_file_path = self.__get_destination_file(Downloader.DOWNLOAD_ROOT_DIR, file_name, date_id)

        if RecoveryInfo(date_id, file_name) in self.downloaded_files:
            self.logger.info('Skip downloaded file {}'.format(final_destination_file_path))
            return

        self.logger.info('Prepare to download {} from url: {}'.format(final_destination_file_path, file_url))
        self.logger.info('File size: {:.2f}MB'.format(total_size / 1e6))

        with http.request('GET', file_url, preload_content=False) as file_reader:
            try:
                downloaded_size = 0
                with open(destination_file_path, 'wb') as destination_file:
                    while True:
                        buffer = file_reader.read(DownloaderConfig.CHUNK_SIZE)
                        downloaded_size += DownloaderConfig.CHUNK_SIZE
                        if not buffer:
                            break
                        destination_file.write(buffer)

                if downloaded_size < total_size:
                    self.logger.error('Download file {} failed from url: {}'.format(file_name, file_url))
                    RecoveryFiles.add_failed_file(date_id, file_name)
                else:
                    self.downloaded_files[RecoveryInfo(date_id, file_name)] = True
                    shutil.move(destination_file_path, final_destination_file_path)

                    DownloadedFiles.add_success_file(date_id, file_name)

                    self.logger.info('Downloaded file {} of {:.2f}MB from {}'.format(
                        final_destination_file_path,
                        total_size / 1e6,
                        file_url
                    ))
            except FileNotFoundError:
                self.logger.error('FileNotFoundError: {}'.format(final_destination_file_path))
                return


class DownloaderConfig:
    CHUNK_SIZE = 16 * 1024
