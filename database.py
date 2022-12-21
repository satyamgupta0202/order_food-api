from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

engine=create_engine('postgresql://myuser:mypass@localhost/mydb',
    echo=True
)
Base = declarative_base()
Session = sessionmaker()