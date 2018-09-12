import datetime
import json
import os
import subprocess

import pytz


def parse_creation_time_from_file(filepath):
    args = 'ffprobe -v quiet -print_format json -select_streams v:0 -show_entries ' \
           'stream=codec_type:format_tags=creation_time ' + filepath
    ffprobe_output = subprocess.check_output(args).decode('utf-8')
    ffprobe_json = json.loads(ffprobe_output)

    creation_time = ffprobe_json['format']['tags']['creation_time']

    local_tz = pytz.timezone('Europe/Amsterdam')
    datetime_without_tz = datetime.datetime.strptime(creation_time, '%Y-%m-%dT%H:%M:%S.000000Z')
    datetime_with_tz = local_tz.localize(datetime_without_tz)
    datetime_string = local_tz.fromutc(datetime_with_tz).strftime('%Y%m%d_%H-%M-%S')

    return datetime_string


def rename_file_to_creation_time(directory, filename):
    creation_time = parse_creation_time_from_file(directory + filename)

    os.rename('{}{}'.format(directory, filename), '{}{}.mp4'.format(directory, creation_time))


rename_file_to_creation_time('C:/Users/denni/Videos/', 'test.MP4')
