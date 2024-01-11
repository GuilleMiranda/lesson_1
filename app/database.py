from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import settings

url = f"postgres://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}"  # "postgresql://fastapi:Tn0Jrx6o4gq3QKT@localhost:5433/course_db"

engine = create_engine(
    url=url,
    #echo=True,  # Prints to standard output the operations (statements) performed.
)

SessionLocal = sessionmaker(autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# try:
#     conn = psycopg2.connect(
#         host="192.168.64.1",
#         port="5432",
#         dbname="fastapi_db",
#         user="postgres",
#         password="postgres",
#         cursor_factory=RealDictCursor,
#     )
#     cursor = conn.cursor()
#     print("Connection done")
# except Exception as error:
#     print(f"Connection failed: {error}")
