import datetime
from pathlib import Path


def datetime_to_second(specific_time):
    return specific_time.hour * 3600 + specific_time.minute * 60 + specific_time.second


def get_date_string(time_delta=0):
    day = datetime.date.today() + datetime.timedelta(days=time_delta)
    return day.strftime('%Y-%m-%d')


def get_previous_working_day_date_id():
    anchor_date = datetime.date(2021, 1, 28)
    anchor_date_id = 4822

    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    while anchor_date < yesterday:
        anchor_date += datetime.timedelta(days=1)
        if anchor_date.strftime('%a') not in ['Sat', 'Sun']:
            anchor_date_id += 1

    return anchor_date_id


def get_date_from_filename(file_name):
    def parse_date(date_string: str):
        return '-'.join([date_string[0:4], date_string[4:6], date_string[6:8]])

    date_length = 4 + 2 + 2

    counter = 0
    date = ''
    for ch in file_name:
        if '0' <= ch <= '9':
            counter += 1
            date += ch
        else:
            counter -= counter
            date = ''
        if counter == date_length:
            return parse_date(date)
    return parse_date('19700101')


def get_file_name(content_disposition):
    parts = [part for part in content_disposition.split(';') if 'filename' in part]
    if len(parts) == 0:
        return ''
    file_name_info = parts[-1]
    return file_name_info.split('=')[-1]


def create_folder(directory):
    Path(directory).mkdir(parents=True, exist_ok=True)
