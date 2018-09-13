import datetime
import os
import subprocess
from datetime import timedelta

import pytz


class FileNotFoundException(Exception):
    pass


def parse_frame_rate_from_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundException(file_path)

    # https://trac.ffmpeg.org/wiki/FFprobeTips
    args = 'ffprobe -v error -select_streams v:0 -show_entries stream=avg_frame_rate -of ' \
           'default=noprint_wrappers=1:nokey=1 {}'.format(file_path)

    ffprobe_output = subprocess.check_output(args).decode('utf-8')

    numerator = ffprobe_output.split('/')[0]
    denominator = ffprobe_output.split('/')[1]
    frame_rate = float(numerator) / float(denominator)
    output = round(frame_rate, 2)

    return output


def parse_duration_from_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundException(file_path)

    args = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {}'.format(file_path)
    ffprobe_output = subprocess.check_output(args).decode('utf-8')

    return float(ffprobe_output)


def parse_start_time_from_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundException(file_path)

    args = 'ffprobe -v error -select_streams v:0 -show_entries stream_tags=creation_time ' \
           '-of default=noprint_wrappers=1:nokey=1 {}'.format(file_path)
    ffprobe_output = subprocess.check_output(args).decode('utf-8')

    local_tz = pytz.timezone('Europe/Amsterdam')
    datetime_without_tz = datetime.datetime.strptime(ffprobe_output, '%Y-%m-%dT%H:%M:%S.000000Z\n')
    datetime_with_tz = local_tz.localize(datetime_without_tz)

    return datetime_with_tz


def datetime_with_tz_to_string(datetime_string, timezone):
    return timezone.fromutc(datetime_string).strftime('%Y%m%d_%H-%M-%S')


def calculate_stop_time_from_file(file_path):
    start_time = parse_start_time_from_file(file_path)
    duration = parse_duration_from_file(file_path)
    stop_time = start_time + timedelta(seconds=float(duration))

    return stop_time


def rename_file_to_start_time(directory, file_name, file_extension):
    file_path = '{}{}.{}'.format(directory, file_name, file_extension)

    if not os.path.isfile(file_path):
        raise FileNotFoundException(directory + file_name)

    creation_time = parse_start_time_from_file(file_path)
    creation_time_string = datetime_with_tz_to_string(creation_time, pytz.timezone('Europe/Amsterdam'))

    os.rename(file_path, '{}{}.{}'.format(directory, creation_time_string, file_extension))


# test_files = ['C:/Users/denni/Videos/20180515_10-00-59.mp4', 'C:/Users/denni/Videos/20180515_12-21-46.mp4']

# rename_file_to_start_time('C:/Users/denni/Videos/', 'test', 'mp4')

# for f in test_files:
#     print(parse_frame_rate_from_file(f))
#     print(parse_start_time_from_file(f))
#     print(parse_duration_from_file(f))
#     print(calculate_stop_time_from_file(f))
#     print()
