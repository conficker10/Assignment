from typing import Mapping
from repositories.train_repository import insert_train_db, fetch_platfrom_no_db, fetch_train_no_db, update_schedule_time_db, update_day_db
import re

regex = "^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"

async def insert_schedule(train_list) -> list:
    response = []
    for train in train_list:
        res_train_no = await get_train_no(train.trainNo)
        res_platform = await fetch_platfrom_no_db(train.platform)
        if res_train_no != None:
            response.append(f'Train No. {train.trainNo} already exists.')
        elif res_platform != None:
            response.append(f'Platform {train.platform} is not available.')
        elif train.platform > 7:
            response.append(f"Platform No. can't be greater than 7")
        elif re.search(regex, train.scheduleTime) == None:
            response.append(f"Invalid Time. Time should be in HH:MM or H:MM Format and in valid range")
        elif check_days(train.day) == False:
            response.append(f"Invalid Day. Day range should be between 1 and 7 inclusive")
        else:
            await insert_train_db(train)
            response.append(f"Succesfully inserted {train.trainNo}")
    return response

async def get_train_no(train_no) -> Mapping:
    return await fetch_train_no_db(train_no)

async def update_train_schedule(train_no, update):
    if re.search(regex, update.scheduleTime) == None:
        return "Invalid Time. Time should be in HH:MM or H:MM Format and in valid range"
    if update.scheduleTime != None:
        await update_schedule_time_db(train_no, update.scheduleTime)
    if update.day != None:
        await update_day_db(train_no, update.day)
    return 'Success'

def check_days(days) -> bool:
    for day in days:
        if day < 1 or day > 7:
            return False
    return True