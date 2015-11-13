from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#engine = create_engine('mysql://root:zaq12wsx@localhost:13306/flask_test?charset=utf8', echo=True)
engine = create_engine('mysql://b3d2d574007570:947ccf7d@us-cdbr-iron-east-03.cleardb.net:3306/ad_db31a335877adb8', echo=True)

DB_Session = sessionmaker(bind=engine)
db_session = DB_Session()
Base = declarative_base()


def init_db():
    import models
    Base.metadata.create_all(bind=engine)


def drop_db():
    Base.metadata.drop_all(engine)


def initial_db():
    drop_db()
    init_db()


if __name__ == '__main__':
    init_db(engine)