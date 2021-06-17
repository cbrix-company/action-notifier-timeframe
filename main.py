import argparse
import os
import sys
from datetime import datetime, timedelta

import pytz


def copy_datetime(dt, time_unit, **kwargs):
    minute = kwargs.get('minute', dt.minute)
    second = kwargs.get('second', dt.second)

    if time_unit == "minutes":
        return datetime(dt.year, dt.month, dt.day, dt.hour, minute, second, tzinfo=pytz.utc)


def current_utc_time():
    return datetime.now(tz=pytz.utc)


def calculate_timeframes(interval, time_unit):
    now = current_utc_time()
    if time_unit == "minutes":
        if now.minute == interval:
            diff = float(now.minute)
            left_minute = diff
        else:
            diff = now.minute / interval
            left_minute = int(diff) * interval

        left_frame = copy_datetime(now, time_unit, minute=int(left_minute), second=0)

        right_frame = left_frame + timedelta(minutes=interval)
        return left_frame, right_frame


def transform_timeframes(left, right):
    """
    05-01-2021-15:03:01
    """
    time_format = '%d-%m-%Y-%H:%M:%S'
    return '{0}#{1}'.format(
        datetime.strftime(left, time_format),
        datetime.strftime(right, time_format)
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--interval', type=int, dest='interval', required=True,  help='interval for time unit')
    parser.add_argument('--time-unit', type=str, dest='time_unit', required=True, help='time unit for interval')

    params = parser.parse_args()

    left, right = calculate_timeframes(params.interval, params.time_unit)
    timeframe = transform_timeframes(left, right)
    print(timeframe)
