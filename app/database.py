from sqlmodel import create_engine, Session
from app.config import DB_SERVER, DB_NAME, DB_USER, DB_PASSWORD

# Exemple de connexion via pyodbc (ODBC Driver 18)
DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}:1433/"
    f"{DB_NAME}?driver=ODBC+Driver+18+for+SQL+Server"
)

engine = create_engine(DATABASE_URL, echo=False)

def get_session():
    """
    Dépendance FastAPI : ouvre une session, puis la referme après usage.
    """
    with Session(engine) as session:
        yield session
