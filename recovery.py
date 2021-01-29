
import utils


class RecoveryInfo:
    SEPARATOR = ';'

    @classmethod
    def from_self_str(cls, line):
        while len(line) > 0 and line[-1] == '\n':
            line = line[:-1]
        return line.split(RecoveryInfo.SEPARATOR)

    def __init__(self, date_id, file_name):
        self.date_id = date_id
        self.file_name = file_name

    def __str__(self):
        return RecoveryInfo.SEPARATOR.join([self.date_id, self.file_name])

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return other.date_id == self.date_id and other.file_name == self.file_name

    def __hash__(self):
        return hash((self.date_id, self.file_name))


class RecoveryFiles:
    FILE_NAME = 'recovery/recovery_{}.txt'

    @classmethod
    def add_failed_file(cls, date_id, file_name):
        with open(RecoveryFiles.FILE_NAME.format(utils.get_date_string()), 'a') as f:
            f.write(''.join(
                [str(RecoveryInfo(date_id, file_name)), '\n']
            ))

    @classmethod
    def get_failed_infos(cls, past_days=1):
        recovery_infos = []
        for i in range(1, past_days + 1):
            with open(RecoveryFiles.FILE_NAME.format(utils.get_date_string(-1 * past_days)), 'a') as f:
                lines = f.readlines()
                for line in lines:
                    date_id, file_name = RecoveryInfo.from_self_str(line)
                    recovery_infos.append(
                        RecoveryInfo(date_id, file_name)
                    )
        return recovery_infos


class DownloadedFiles:
    FILE_NAME = 'success.txt'

    @classmethod
    def add_success_file(cls, date_id, file_name):
        with open(DownloadedFiles.FILE_NAME, 'a') as f:
            f.write(''.join(
                [str(RecoveryInfo(date_id, file_name)), '\n']
            ))

    @classmethod
    def load_success_files(cls):
        success_files = {}
        with open(DownloadedFiles.FILE_NAME, 'a') as f:
            lines = f.readlines()
            for line in lines:
                date_id, file_name = RecoveryInfo.from_self_str(line)
                success_files[RecoveryInfo(date_id, file_name)] = True
        return success_files
