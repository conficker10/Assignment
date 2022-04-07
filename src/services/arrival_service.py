from repositories.arrival_repository import update_arrival_time_db, fetch_train_no_with_arrival_db
from repositories.train_repository import fetch_train_no_db
import datetime
import re

async def update_arrival_time(train_no, arrival_time) -> str:
    regex = "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"
    res = await fetch_train_no_db(train_no)
    val = dict(res.items())
    diff = calculate_time_diff(val['scheduleTime'], arrival_time)
    diff_in_mins = abs(int(diff.split(':')[0]) * 60) + int(diff.split(':')[1])
    if diff[0] == '-' and diff_in_mins > 60:
        return "Invalid Time. Arrival Time cannot be more than 1 hour before schedule time"
    if re.search(regex, arrival_time) == None:
        return "Invalid Time. Time should be in HH:MM or H:MM Format and in valid range"
    
    await update_arrival_time_db(train_no, arrival_time)
    return f"Updated Arrival for Train No.: {train_no}"

async def get_time_diff(train) -> dict:
    diff = calculate_time_diff(train['scheduleTime'], train['arrivalTime'])
    response = {
        'scheduleTime': train['scheduleTime'],
        'arrivalTime': train['arrivalTime'],
        'timeDiff': diff
    }
    return response

async def get_all_time_diff() -> list:
    response = []
    res = await fetch_train_no_with_arrival_db()
    for rec in res:
        val = dict(rec.items())
        temp = await get_time_diff(val)
        temp["trainNo"] = val['trainNo']
        response.append(temp)
    return response


def calculate_time_diff(schedule_time, arrival_time) -> str:
    format = '%H:%M'
    s_time = datetime.datetime.strptime(schedule_time, format)
    a_time = datetime.datetime.strptime(arrival_time, format)
    res = ""
    if a_time < s_time:
        a_time ,s_time = s_time, a_time
        res = res + "-"
    diff = a_time - s_time
    res = res + str(diff)[:-3]
    return res