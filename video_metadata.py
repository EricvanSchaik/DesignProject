import datetime
import json
import os
import subprocess

import pytz


class FileNotFoundException(Exception):
    pass


def parse_creation_time_from_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundException(file_path)

    args = 'ffprobe -v quiet -print_format json -select_streams v:0 -show_entries ' \
           'stream=codec_type:format_tags=creation_time ' + file_path
    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    ffprobe_json = json.loads(ffprobe_output)

    creation_time = ffprobe_json['format']['tags']['creation_time']

    local_tz = pytz.timezone('Europe/Amsterdam')
    datetime_without_tz = datetime.datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%S.000000Z')
    datetime_with_tz = local_tz.localize(datetime_without_tz)
    datetime_string = local_tz.fromutc(datetime_with_tz).strftime('%Y%m%d_%H-%M-%S')

    return datetime_string


def rename_file_to_creation_time(directory, file_name, file_extension):
    file_path = '{}{}.{}'.format(directory, file_name, file_extension)
    if not os.path.isfile(file_path):
        raise FileNotFoundException(directory + file_name)

    creation_time = parse_creation_time_from_file(file_path)

    os.rename(file_path, '{}{}.{}'.format(directory, creation_time, file_extension))


rename_file_to_creation_time('C:/Users/denni/Videos/', 'test', 'mp4')
