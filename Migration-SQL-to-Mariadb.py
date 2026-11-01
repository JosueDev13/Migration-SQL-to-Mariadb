import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import URL

# Conexiones

#De SQL Server(Usando docker para correrlo)
mssql_url = URL.create(
    "mssql+pymssql",
    username="sa",
    password="SqlPassword2026",
    host="localhost",
    port=1433,
    database="db_pr0",
)
#Referencia para Mariadb

mysql_url = URL.create(
    "mysql+pymysql",
    username="Saib",
    password="$aib@13",   
    host="localhost",
    port=3306,
    database="db_pr0",
)

mssql = create_engine(mssql_url)
mysql = create_engine(mysql_url)



inspector = inspect(mssql)

# for tabla in inspector.get_table_names():
#   print(f"Migrando {tabla}...")
#   primera = True
 #   for chunk in pd.read_sql_table(tabla, mssql, chunksize=10000):
  #      chunk.to_sql(
   #         tabla,
    #        mysql,
     #       if_exists="replace" if primera else "append",
      #      index=False,
       # )
        #primera = False


fallidas = []

for tabla in inspector.get_table_names():
    print(f"Migrando {tabla}...")
    try:
        primera = True
        for chunk in pd.read_sql_table(tabla, mssql, chunksize=10000):
            chunk.columns = [c.strip() for c in chunk.columns]
            chunk.to_sql(
                tabla,
                mysql,
                if_exists="replace" if primera else "append",
                index=False,
            )
            primera = False
    except Exception as e:
        print(f"   ERROR en {tabla}: {str(e)[:150]}")
        fallidas.append(tabla)

print("\nListo")
if fallidas:
    print("Tablas con error:", fallidas);


print("Listo")
