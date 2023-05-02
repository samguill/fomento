from django.utils.timezone import localtime
from dateutil import parser
from decimal import Decimal
from datetime import datetime
from typing import Any

import pytz

def utc_to_local_time(date_to_format):
    try:
        time_zone = date_to_format.tzinfo
        if time_zone:
            date_to_format = localtime(date_to_format, time_zone)
    except Exception as e:
        pass
    return date_to_format


def report_date_format(date_to_format, format=None, default_value="", local=True):
    if date_to_format is None:
        return default_value

    if isinstance(date_to_format, str):
        try:
            date_to_format = parser.parse(date_to_format)
        except Exception as e:
            return default_value

    elif isinstance(date_to_format, list):
        for x in date_to_format:
            if isinstance(x, str):
                return "\n ".join([localtime(utc_to_local_time(parser.parse(x))).strftime("%b %d, %Y")])
            elif format == "datetime":
                return "\n ".join([localtime(utc_to_local_time(parser.parse(x))).strftime("%b %d, %Y %H:%M")])
            else:
                return x.strftime("%b %d, %Y")

    if local is True:
        date_to_format = utc_to_local_time(date_to_format)

    if isinstance(date_to_format, (datetime.date, datetime.datetime)):
        if format == "parsed":
            return date_to_format
        elif format == "parsed_tz":
            return date_to_format.replace(tzinfo=pytz.UTC)
        elif format == "datetime":
            return date_to_format.strftime("%b %d, %Y %H:%M")
        else:
            return date_to_format.strftime("%b %d, %Y")

    return default_value


def to_boolean(value) -> bool:
    if isinstance(value, str):
        false_values = ("0", "f", "", "false", "falso", "n", "no", "null", "none")
        return value.lower() not in false_values
    else:
        return bool(int(value))


def get_from_dict(
    dictionary,
    key,
    default_if_not_exist=None,
    default_if_empty: Any = "",
    strip_value=True,
    cast_function=None,
):
    try:
        try:
            value = dictionary[key]
            if (
                not isinstance(value, bool)
                and value is None
                or (strip_value is True and isinstance(value, str) and len(value.strip()) == 0)
                or (isinstance(value, list) and not value)
            ):
                return default_if_empty
            if cast_function:
                if cast_function == "to_datetime_str":
                    value = report_date_format(date_to_format=value, format="datetime")
                elif cast_function == "to_date_str":
                    value = report_date_format(date_to_format=value)
                elif cast_function == "to_datetime":
                    if isinstance(value, str):
                        value = parser.parse(value)
                elif cast_function == "to_date":
                    if isinstance(value, str):
                        value = parser.parse(value).date()
                elif cast_function is bool:
                    value = to_boolean(value)
                elif cast_function == "comma_separated":
                    if isinstance(value, int):
                        value = str(value)
                    if isinstance(value, str):
                        value = [_f for _f in value.split(",") if _f]
                elif cast_function == "decimal":
                    value = Decimal(value)
                else:
                    return cast_function(value)
            return value
        except KeyError:
            return default_if_not_exist
    except Exception as e:
        return default_if_not_exist
