from typing import Mapping
from repositories.models.train import trainData
from db.database import database

async def fetch_train_no_db(train_no) -> Mapping:
    query = trainData.select().where(trainData.c.trainNo == train_no)
    return await database.fetch_one(query)

async def fetch_platfrom_no_db(platform) -> Mapping:
    query = trainData.select().where(trainData.c.platform == platform)
    return await database.fetch_one(query)

async def insert_train_db(train) -> None:
    query = trainData.insert().values(trainNo=train.trainNo, scheduleTime=train.scheduleTime, day = train.day, platform = train.platform)
    await database.execute(query)

async def update_schedule_time_db(train_no, schedule_time) -> None:
    query = trainData.update().where(trainData.c.trainNo == train_no).values(scheduleTime=schedule_time)
    await database.execute(query)

async def update_day_db(train_no, day) -> None:
    query = trainData.update().where(trainData.c.trainNo == train_no).values(day=day)
    await database.execute(query)