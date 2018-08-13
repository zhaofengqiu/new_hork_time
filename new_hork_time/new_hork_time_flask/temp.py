from config import *
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from models import New,User,Article

def init():
    global session
    engine = create_engine(DB_URI)
    Session=sessionmaker(bind=engine)
    session=Session()
    new=session.query(Article).first()
    print(new.text)

