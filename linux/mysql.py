# -*- coding:utf-8 -*-
from sqlalchemy import create_engine, UniqueConstraint, Index
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


engine = create_engine("mysql+pymysql://root:root@localhost:3306/food", encoding="utf-8", echo=False)
Base = declarative_base()
