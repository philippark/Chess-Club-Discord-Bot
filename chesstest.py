import schedule
import time

def job(t):
    print ("I'm working...", t)
    return

schedule.every().day.at("01:23").do(job,'It is 01:00')

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute