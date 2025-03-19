import schedule
import time
from web_scraper import find_free_funds
import sqlite3

def job():
    funds = find_free_funds()
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        for fund in funds:
            cursor.execute('INSERT INTO funds (amount, description) VALUES (?, ?)', (fund['amount'], fund['description']))
        conn.commit()

schedule.every().day.at("00:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
