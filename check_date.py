from datetime import datetime, timedelta


def check_ptt_date(ptt_date_string, before_days_count):
  #ptt_date_string='Wed Jan 14 09:36:59 2019'

  ptt_dt = ptt_date_string.split(' ')

  i_month=0
  i_year=int(ptt_dt[4])
  i_day=int(ptt_dt[2])

  if (ptt_dt[1]=='Jan'):
    i_month=1
  if (ptt_dt[1]=='Feb'):
    i_month=2
  if (ptt_dt[1]=='Mar'):
    i_month=3
  if (ptt_dt[1]=='Apr'):
    i_month=4
  if (ptt_dt[1]=='May'):
    i_month=5
  if (ptt_dt[1]=='Jun'):
    i_month=6
  if (ptt_dt[1]=='Jul'):
    i_month=7
  if (ptt_dt[1]=='Aug'):
    i_month=8
  if (ptt_dt[1]=='Sep'):
    i_month=9
  if (ptt_dt[1]=='Oct'):
    i_month=10
  if (ptt_dt[1]=='Nov'):
    i_month=11
  if (ptt_dt[1]=='Dec'):
    i_month=12


  ptt_date = datetime(i_year, i_month, i_day)

  today = datetime(datetime.today().year, datetime.today().month, datetime.today().day)

  dt = today.date() - ptt_date.date()

  is_check=False

  if (dt.total_seconds() > (before_days_count*24*60*60)):
    is_check=True

  return is_check
