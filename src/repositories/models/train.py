from sqlalchemy import ForeignKey
import sqlalchemy
from db.database import metadata

trainData = sqlalchemy.Table(
    "trainData",
    metadata,
    sqlalchemy.Column("trainNo", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("scheduleTime", sqlalchemy.String),
    sqlalchemy.Column("arrivalTime", sqlalchemy.String),
    sqlalchemy.Column("day", sqlalchemy.ARRAY(sqlalchemy.Integer)),
    sqlalchemy.Column("platform", sqlalchemy.Integer),
)

arrivalTimeData = sqlalchemy.Table(
    "arrivalTimeData",
    metadata,
    sqlalchemy.Column("trainNo", sqlalchemy.Integer, ForeignKey("trainData.trainNo")),
    sqlalchemy.Column("arrivalTime", sqlalchemy.String),
)