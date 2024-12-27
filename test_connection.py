import pyodbc

server = "adventureworks-server-hdf.database.windows.net"
database = "FABADI-db"
username = "jvcb"
password = "cbjv592023!"
driver = "ODBC Driver 18 for SQL Server"

try:
    conn = pyodbc.connect(
        f"DRIVER={{{driver}}};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password};Encrypt=YES;TrustServerCertificate=YES;Connection Timeout=60"
    )
    print("Connexion réussie à la base de données !")
except pyodbc.InterfaceError as e:
    print("Erreur de connexion :", e)
except Exception as e:
    print("Une autre erreur est survenue :", e)
