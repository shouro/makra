from sqlalchemy import create_engine, Column
from sqlalchemy import ARRAY, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql.json import JSONB
from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(
                get_project_settings().get("POSTGRES_CONNECTION_STRING")
        )


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Article(DeclarativeBase):
    __tablename__ = "article_table"

    id = Column(Integer, primary_key=True)
    uid = Column('uid', String)
    url = Column('url', String)
    status = Column('status', Integer)
    domain = Column('domain', String)
    indexing_timestamp = Column('indexing_timestamp', DateTime, nullable=True)
    lang_detected = Column('lang_detected', String)
    images = Column('images', JSONB)
    videos = Column('videos', JSONB)
    title = Column('title', String)
    category = Column('category', String)
    author = Column('author', String)
    date_published = Column('date_published', DateTime, nullable=True)
    date_modified = Column('date_modified', DateTime, nullable=True)
    article = Column('article', Text)
    tags = Column('tags', ARRAY(String))
    comments = Column('comments', JSONB)
