import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

engine = create_engine(os.getenv('DATABASE_URL'))
conn = engine.connect()

res = conn.execute(text("SELECT now()")).fetchall()
print(res)