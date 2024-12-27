import pyodbc
import os
from dotenv import load_dotenv
env_path = os.path.join(".env")
load_dotenv(dotenv_path=env_path, override=True)

server =  os.getenv("DB_SERVER")
database = os.getenv("DB_NAME")
username = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
driver = os.getenv("ODBC_DRIVER")

try:
    conn = pyodbc.connect(
        f"DRIVER={{{driver}}};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=YES;TrustServerCertificate=YES;Connection Timeout=60"
    )
    print("Connexion réussie à la base de données !")
except pyodbc.InterfaceError as e:
    print("Erreur de connexion :", e)
except Exception as e:
    print("Une autre erreur est survenue :", e)
