#!/usr/bin/env python3
# delete_items.py
from database_sql import SessionLocal, SQLItem

def delete_all_items():
    db = SessionLocal()
    try:
        # Delete all records from the SQLItem table
        deleted_count = db.query(SQLItem).delete()
        db.commit()
        print(f"Deleted {deleted_count} records from the PostgreSQL database.")
    except Exception as e:
        db.rollback()
        print("An error occurred:", e)
    finally:
        db.close()

if __name__ == "__main__":
    delete_all_items()
