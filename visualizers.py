
class ProgressVisualizer():
    def __init__(self, total_size):
        self.total_file_size = total_size
        self.downloaded_file_size = 0
        self.previous_percent = 0
        self.current_percent = 0

        print('Will download {0:.2f} MB'.format(total_size / 1e6))
        self.visualize_progress()

    def visualize_progress(self, downloaded_chunk=0):
        self.downloaded_file_size += downloaded_chunk
        self.current_percent = 100 * self.downloaded_file_size / self.total_file_size
        if self.current_percent - self.previous_percent >= 2:
            print('Downloaded: {}'.format(str(self)))
            self.previous_percent = self.current_percent

    def __str__(self):
        return '{0:.2f}/{1:.2f} ({2:.2f}%)'.format(self.downloaded_file_size / 1e6,
                                                   self.total_file_size / 1e6,
                                                   self.current_percent)

    def __enter__(self):
        if self.total_file_size <= 0:
            raise ValueError
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.visualize_progress()
