import os
import asyncio

from sqlalchemy import text

from app.app_sql.setup_database import SessionLocal
from app.services.sql import ScheduleDecisionCrud


async def run():
    await asyncio.to_thread(initialization)

def initialization():
    with open(os.path.join(os.getcwd(), "app/app_sql/initialization.sql"), 'r') as file:
        sql_commands = file.read()

    db = SessionLocal()
    try:
        if ScheduleDecisionCrud.countAll(db) == 0:
            # Execute each command in the SQL file
            for command in sql_commands.split(';'):
                command = command.strip()
                if command:
                    db.execute(text(command))
            db.commit()
            print("Initialize database successfully")
    except Exception as e:
        db.rollback()
        print(f"An error occurred: {e}")
    finally:
        db.close()