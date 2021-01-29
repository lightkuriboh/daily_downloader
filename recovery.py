
class ErrorLogMessage:
    SEPARATOR = ';'

    def __init__(self, date_string, file_name, msg):
        self.date_string = date_string
        self.file_name = file_name
        self.msg = msg

    def __str__(self):
        return ErrorLogMessage.SEPARATOR.join([self.date_string, self.file_name, self.msg])

    def __repr__(self):
        return self.__str__()
