#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from enum import Enum, unique
from lib import unicode_character_align_east_asian as uca
import datetime as dt

MESSAGE_TYPE = unique(Enum(
    'MESSAGE_TYPE', (
        'NORMAL', 'WARNING', 'ERROR'
    )
))


def print_banner(
    message: str,
    message_type: MESSAGE_TYPE = MESSAGE_TYPE.NORMAL,
    width: int = 80,
    upper_case: bool = True,
    border: str = None,
    fill: str = None,
    align: str = None,
    include_timestamp: bool = False,
) -> str:
    if upper_case:
        message = message.upper()

    if border is None:
        border = '#' if (message_type is MESSAGE_TYPE.NORMAL) else '!'
    if fill is None:
        fill = ' '
    if align is None:
        align = '^'

    message_line_format = ''
    fill_width = 0

    if message_type is MESSAGE_TYPE.NORMAL:
        message_line_format = '{border}{message:{fill}{align}{fill_width}}{border}'
        fill_width = width - len(border) * 2 - (uca.count_visual_length(message) - len(message))
    elif message_type is MESSAGE_TYPE.WARNING:
        message_line_format = ''.join(
            ('{border}' * 3, '{message:{fill}{align}{fill_width}}', '{border}' * 3,)
        )
        fill_width = width - len(border) * 3 * 2 - (uca.count_visual_length(message) - len(message))
    elif message_type is MESSAGE_TYPE.ERROR:
        message = fill * 3 + message + fill * 3
        message_line_format = '{message:{border}{align}{fill_width}}'
        fill_width = width - len(fill) * 3 * 2 - (uca.count_visual_length(message) - len(message))

    banner = '\n'.join((
        '{edge}{timestamp:{border}^{fill_width}}{edge}'.format(
            edge=border * 2,
            timestamp=' {} '.format(
                '{} {} {}'.format((
                    t := dt.datetime.now(dt.timezone.utc).isoformat(timespec='milliseconds')
                )[0:10], t[11:23], t[23:], ),
            ),
            border=border,
            fill_width=width - len(border) * 2 * 2,
        ) if include_timestamp else border * width,
        message_line_format.format(
            border=border, message=message, fill=fill, align=align, fill_width=fill_width,
        ),
        border * width,
    ))

    print(banner)
    return banner
