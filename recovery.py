
import os.path

import utils


class RecoveryInfo:
    SEPARATOR = ';'

    @classmethod
    def from_self_str(cls, line):
        while len(line) > 0 and line[-1] == '\n':
            line = line[:-1]
        return line.split(RecoveryInfo.SEPARATOR) if line else (None, None)

    def __init__(self, date_id, file_name):
        self.date_id = str(date_id)
        self.file_name = file_name

    def __str__(self):
        return RecoveryInfo.SEPARATOR.join([self.date_id, self.file_name])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return other.date_id == self.date_id and other.file_name == self.file_name

    def __hash__(self):
        return hash((self.date_id, self.file_name))


class DownloadedFiles:
    FILE_NAME = 'recovery/success.txt'

    @classmethod
    def add_success_file(cls, date_id, file_name):
        with open(DownloadedFiles.FILE_NAME, 'a') as f:
            f.write(''.join(
                [str(RecoveryInfo(date_id, file_name)), '\n']
            ))

    @classmethod
    def load_success_files(cls):
        success_files = {}
        if not os.path.exists(DownloadedFiles.FILE_NAME):
            utils.create_file(DownloadedFiles.FILE_NAME)

        with open(DownloadedFiles.FILE_NAME, 'r') as f:
            lines = f.readlines()
            for line in lines:
                date_id, file_name = RecoveryInfo.from_self_str(line)
                if date_id is not None and file_name is not None:
                    success_files[RecoveryInfo(date_id, file_name)] = True
        return success_files


class RecoveryFiles:
    FILE_NAME = 'recovery/recovery_{}.txt'

    @classmethod
    def add_failed_file(cls, date_id, file_name):
        with open(RecoveryFiles.FILE_NAME.format(utils.get_date_string()), 'a') as f:
            f.write(''.join(
                [str(RecoveryInfo(date_id, file_name)), '\n']
            ))

    @classmethod
    def load_failed_infos(cls, past_days=1):
        recovery_infos = []

        for i in range(1, past_days + 1):
            recovery_file = RecoveryFiles.FILE_NAME.format(utils.get_date_string(-1 * i))

            if not os.path.exists(recovery_file):
                utils.create_file(recovery_file)

            with open(recovery_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    date_id, file_name = RecoveryInfo.from_self_str(line)
                    if date_id is not None and file_name is not None:
                        recovery_infos.append(
                            RecoveryInfo(date_id, file_name)
                        )
        return set(recovery_infos)


def retry_download(downloader, past_days=1):
    downloader.logger.info('Start recovering')
    recovery_infos = RecoveryFiles.load_failed_infos(past_days)
    for recovery_info in recovery_infos:
        downloader.logger.info('Retrying to download file {}'.format(recovery_info.file_name))
        downloader.download(recovery_info.file_name, recovery_info.date_id)
    downloader.logger.info('Finish recovering')
