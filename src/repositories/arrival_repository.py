from typing import Mapping
from repositories.models.train import trainData, arrivalTimeData
from db.database import database
from typing import List

async def update_arrival_time_db(train_no, arrival_time) -> None:
    query = trainData.update().where(trainData.c.trainNo == train_no).values(arrivalTime=arrival_time)
    await database.execute(query)
    query = arrivalTimeData.insert().values(trainNo=train_no, arrivalTime=arrival_time)
    await database.execute(query)

async def fetch_train_no_with_arrival_db() -> List[Mapping]:
    query = trainData.select().where(trainData.c.arrivalTime != None)
    return await database.fetch_all(query)