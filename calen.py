#!/usr/bin/env python3
import calendar
from datetime import date, timedelta
import jpholiday
import os
import sys
import re
import webbrowser
import os


def get_last_date(dt):
    return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])


def month_year_iter(start_month, start_year, end_month, end_year):
    ym_start = 12*start_year + start_month - 1
    ym_end = 12*end_year + end_month
    for ym in range(ym_start, ym_end):
        y, m = divmod(ym, 12)
        yield y, m+1


since = date.today().replace(day=1)
until = get_last_date(date.today().replace(day=1) + timedelta(days=500))
holidays = jpholiday.between(since, until)
calendar.LocaleHTMLCalendar.cssclasses = [
    "mon text-bold", "tue", "wed", "thu", "fri", "sat blue", "sun red"
]
calendar.LocaleHTMLCalendar.cssclass_month_head = 'month_head'
if sys.platform == 'win32':
    locale = 'ja_JP'
else:
    locale = 'ja_JP.UTF-8'
calendar_html = calendar.LocaleHTMLCalendar(firstweekday=6, locale=locale)

script_dir = os.path.dirname(os.path.realpath(__file__))

document = f'''
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="{script_dir}/calen.css" />
<title>Calendar for 2023</title>
</head>
<body>
'''

for year, month in month_year_iter(since.month, since.year, until.month, until.year):
    month_cal = '<div class="month_cal">' + calendar_html.formatmonth(year, month)
    holidays_div = ''
    for holiday in filter(lambda h: h[0].year == year and h[0].month == month, holidays):
        h_month = holiday[0].month
        h_day = holiday[0].day
        month_cal = re.sub(
            r'(?<=<td class=")(.+?)(?=">' + str(h_day) + '</td>)',
            r'\1 holiday',
            month_cal
        )
        holidays_div += '<li>' + f'{h_month}月{h_day}日: ' + holiday[1] + '</li>'
    document += month_cal + '<ul class="holidays">' + holidays_div + '</ul></div>'

document += '</body></html>'

with open('calen.html', 'w', encoding='utf-8') as f:
    f.write(document)

webbrowser.open(os.path.realpath('calen.html'))
