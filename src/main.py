from fastapi import FastAPI, status
from typing import List
from dtos.train import Train, TrainUpdate, TrainUpdateSchedule
from db.database import database
from services.train_service import insert_schedule, get_train_no, update_train_schedule
from services.arrival_service import update_arrival_time, get_all_time_diff, get_time_diff

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()



@app.post("/schedule",  status_code = status.HTTP_201_CREATED)
async def create_schedule(train_list: List[Train]):
    return await insert_schedule(train_list)

@app.post("/train-arrival/{trainNo}",  status_code = status.HTTP_200_OK)
async def update_arrival(trainNo: int, update: TrainUpdate):
    res_train_no = await get_train_no(trainNo)
    if res_train_no == None:
        return "Invalid Train No."
    return await update_arrival_time(trainNo, update.arrivalTime)

@app.put("/train-schedule/{trainNo}",  status_code = status.HTTP_200_OK)
async def update_schedule(trainNo: int, update: TrainUpdateSchedule):
    res_train_no = await get_train_no(trainNo)
    if res_train_no == None:
        return "Invalid Train No."
    if(update.scheduleTime == None and update.day == None):
        return 'Invalid Format. Pass atleast one of scheduleTime or day'
    return await update_train_schedule(trainNo, update)

@app.get('/time-diff', status_code = status.HTTP_200_OK)
async def get_all_trains() -> list:
    return await get_all_time_diff()

@app.get('/time-diff/{trainNo}', status_code = status.HTTP_200_OK)
async def get_trains(trainNo: int):
    res = await get_train_no(trainNo)
    if res == None:
        return "Invalid Train No."
    val = dict(res.items())
    if val['arrivalTime'] == None:
        return "There is no difference. Arrival Time is None"
    return await get_time_diff(val)