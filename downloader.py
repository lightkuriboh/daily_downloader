import urllib3

CHUNK_SIZE = 16 * 1024


class ProgressVisualizer():
    def __init__(self, total_size):
        self.total_file_size = total_size
        self.downloaded_file_size = 0
        self.previous_percent = -1.0

        print('Will download {0:.2f} MB'.format(total_size / 1e6))
        self.visualize_progress()

    def visualize_progress(self, downloaded_chunk=0):
        self.downloaded_file_size += downloaded_chunk
        current_percent = 100 * self.downloaded_file_size / self.total_file_size
        if current_percent - self.previous_percent >= 2:
            print('Downloaded: {0:.2f}/{1:.2f} ({2:.2f}%)'.format(self.downloaded_file_size / 1e6,
                                                                  self.total_file_size / 1e6,
                                                                  current_percent))
            self.previous_percent = current_percent

    def __enter__(self):
        if self.total_file_size <= 0:
            raise ValueError
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def get_file_size(file_url, connection):
    file_reader = connection.urlopen('HEAD', file_url)
    if file_reader.info()['Content-Type'] != 'application/download':
        return None
    return int(file_reader.info()['Content-Length'])


def download_file(file_url, destination_file_path):
    http = urllib3.PoolManager()
    total_size = get_file_size(file_url, http)

    with ProgressVisualizer(total_size) as progress_logger:
        with http.request('GET', file_url, preload_content=False) as file_reader:
            with open(destination_file_path, 'wb') as destination_file:
                while True:
                    buffer = file_reader.read(CHUNK_SIZE)
                    if not buffer:
                        break
                    destination_file.write(buffer)
                    progress_logger.visualize_progress(CHUNK_SIZE)
