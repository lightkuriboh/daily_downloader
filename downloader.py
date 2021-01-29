import urllib3


class Downloader:
    DOWNLOAD_CONTENT_TYPES = ['application/octet-stream', 'application/download']

    def __init__(self, logger):
        self.logger = logger

    def get_file_size(self, file_url, connection):
        file_getter = connection.urlopen('HEAD', file_url)
        print(file_getter.info())
        if file_getter.info()['Content-Type'] not in Downloader.DOWNLOAD_CONTENT_TYPES:
            self.logger.error('File not found: {}'.format(file_url))
            return None
        return int(file_getter.info()['Content-Length'])

    def download(self, file_url, destination_file_path):
        http = urllib3.PoolManager()
        total_size = self.get_file_size(file_url, http)
        if not total_size:
            return
        if total_size > 1e9:
            self.logger.warn('Large file size: {}MB from url: {}'.format(total_size / 1e6, file_url))

        self.logger.info('Prepare to download {} from url: {}'.format(destination_file_path, file_url))
        self.logger.info('File size: {:.2f}MB'.format(total_size / 1e6))

        with http.request('GET', file_url, preload_content=False) as file_reader:
            try:
                with open(destination_file_path, 'wb') as destination_file:
                    while True:
                        buffer = file_reader.read(DownloaderConfig.CHUNK_SIZE)
                        if not buffer:
                            break
                        destination_file.write(buffer)
            except FileNotFoundError:
                self.logger.error('FileNotFoundError: {}'.format(destination_file_path))
                return

        self.logger.info('Downloaded file {} of {:.2f}MB from {}'.format(
            destination_file_path,
            total_size / 1e6,
            file_url
        ))


class DownloaderConfig:
    CHUNK_SIZE = 16 * 1024
