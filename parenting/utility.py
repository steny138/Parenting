import pytz
from datetime import datetime as dt
from datetime import timedelta


def to_timestamp(minutes=0):
    """ now datetime to timestamp

    Returns:
        timestamp (int): timestamp in seconds
    """
    now = dt.now(pytz.timezone('Asia/Taipei')) + timedelta(minutes=minutes)

    return dt.timestamp(now)  # 轉成時間戳


def now_timestamp():
    """ now datetime to timestamp

    Returns:
        timestamp (int): timestamp in seconds
    """
    now = dt.now(pytz.timezone('Asia/Taipei'))
    return dt.timestamp(now)  # 轉成時間戳
