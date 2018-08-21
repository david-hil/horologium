#!/usr/bin/env python3
import argparse
import sqlite3
import os.path
import time
import helper

parser = argparse.ArgumentParser(description="A simple time stamp clock for the command line")
parser.add_argument("command", help="the command that will be executed", choices=['start','stop', 'status', 'log'])
parser.add_argument("-l", "--label", help="the label of the task you're working on (use this for categories like \"Work\")")
parser.add_argument('-t', '--task', help="the task you're working on (use this as a specific description like \"Finishing feature x\")")
parser.add_argument("-n", '--number', help="how many of the last tasks horologium log shows (default is 3)", type=int, default=3)

if os.path.isfile('stechuhr.db'):
    db = sqlite3.connect("stechuhr.db")
    cursor = db.cursor()
else:
    db = sqlite3.connect("stechuhr.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE status(date real, label text, task text)")
    cursor.execute("CREATE TABLE history(date real, label text, task text, time real)")
db.commit()

args = parser.parse_args()



def start():
    cursor.execute("SELECT * FROM status")
    if cursor.fetchone():
        print("You're already working on a task. For more info, use horologium status")
        return
    cursor.execute("INSERT INTO status VALUES (?,?,?)", (time.time(), args.label, args.task))
    print("Started time measurement for {}{}.".format(args.task if args.task else "task", " [{}]".format(args.label) if args.label else ""))
    cursor.execute
    db.commit()

def status():
    cursor.execute("SELECT * FROM status")
    task = cursor.fetchone()
    if not task:
        print("You aren't currently working on a task. Use horologium start to start working.")
    else:
        timepassed = time.time() - task[0]
        print("You're working on " + helper.parseTask(task) + "for" + helper.parseTime(timepassed))

def stop():
    cursor.execute("SELECT * FROM status")
    task = cursor.fetchone()
    if not task:
        print("You aren't currently working on a task. Use horologium start to start working.")
    else:
        timepassed = time.time() - task[0]
        cursor.execute("INSERT INTO history VALUES (?,?,?,?)", (task[0],task[1],task[2],timepassed))
        db.commit()
        cursor.execute("DELETE FROM status WHERE 1=1")
        db.commit()
        print("You were working on " + helper.parseTask(task) + "for" + helper.parseTime(timepassed))

def log():
    cursor.execute("SELECT * FROM history ORDER BY date DESC LIMIT ?", str(args.number))
    rows = cursor.fetchall()
    for task in rows:
        print("On " + time.asctime(time.localtime(task[0])) + " you worked for " + helper.parseTime(task[3]) + " on " + helper.parseTask(task))



functions = {"start": start, "status": status, "stop": stop, "log" : log}
functions[args.command]()

db.close()

