import configparser
import codecs
import json
import re

from datetime import datetime

from .users import User


def build_config(config_name='config.ini') -> None:
    """Build default config section key/values"""
    config = configparser.ConfigParser()
    config.update({
        'MAIN': {
            'debug': True,
        },
        'TELEGRAM': {
            'api_token': '',
            'developer_id': '',
            'manager_password': 1234,
        },
    })
    with open(config_name, 'w') as f:
        print('- Creating new config')
        config.write(f)


def load_config(config_fp='config.ini'):
    """load config from `config_fp`; build default if not found"""
    config = configparser.ConfigParser()
    try:
        config.read_file(codecs.open(config_fp, 'r', 'utf8'))
    except FileNotFoundError:
        print('- Config not found')
        build_config()
        config.read_file(codecs.open(config_fp, 'r', 'utf8'))
    return config


def handle_error(error, to_file=False, to_file_path='error_log.txt'):
    """Handle error by writing to file/sending to sentry/raising"""
    if to_file:
        with open(to_file_path, 'a', encoding='utf-8') as f:
            f.write(error + '\n')
    else:
        raise error


def load_json(file_path: str) -> list[dict]:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def update_json_file(data, file_path, mode='w'):
    with open(f'{file_path}', mode, encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)


def slice_sheet_dates(date: str) -> tuple[list[int], str]:
    """Отформатировать строку слов/времени к datetime формату"""
    sheet_days = {
        'ежедневно': range(0, 7),
        'будние': range(0, 5),
        'понедельник': 0,
        'вторник': 1,
        'среда': 2,
        'четверг': 3,
        'пятница': 4,
        'суббота': 5,
        'воскресенье': 6,
    }
    days = []
    for day in sheet_days:
        if day in date.lower():
            try:
                days += sheet_days[day]
            except TypeError:
                days.append(sheet_days[day])
    sheet_time = re.search(r'\d+:\d+', date)[0]
    return (days, sheet_time)


def format_cleaning_date(date: tuple[list[int], str]) -> str:
    today = datetime.today()
    for day in date[0]:
        if day != today.weekday():
            continue
        job_at = f'{today.date()} {date[1]}:00'
        return job_at
