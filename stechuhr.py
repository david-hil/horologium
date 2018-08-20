#!/usr/bin/env python3
import argparse
import sqlite3
import os.path
import time
import math
import helper

parser = argparse.ArgumentParser(description="A simple time stamp clock for the command line")
parser.add_argument("command", help="the command that will be executed", choices=['start','stop', 'status'])
parser.add_argument("-l", "--label", help="the label of the task you're working on (use this for categories like \"Work\")")
parser.add_argument('-t', '--task', help="the task you're working on (use this as a specific description like \"Finishing feature x\")")

if os.path.isfile('stechuhr.db'):
    db = sqlite3.connect("stechuhr.db")
    cursor = db.cursor()
else:
    db = sqlite3.connect("stechuhr.db")
    cursor = db.cursor()
    cursor.execute("CREATE TABLE status(date text, label text, task text)")
    cursor.execute("CREATE TABLE history(date text, label text, task text, time real)")
db.commit()

args = parser.parse_args()



def start():
    cursor.execute("SELECT * FROM status")
    if cursor.fetchone():
        print("You're already working on a task. For more info, use horologium status")
        return
    cursor.execute("INSERT INTO status VALUES (?,?,?)", (time.asctime(time.localtime(time.time())), args.label, args.task))
    print("Started time measurement for {}{}.".format(args.task if args.task else "task", " [{}]".format(args.label) if args.label else ""))
    db.commit()

def status():
    cursor.execute("SELECT * FROM status")
    task = cursor.fetchone()
    if not task:
        print("You aren't currently working on a task. Use horologium start to start working.")
    else:
        timepassed = time.time() - time.mktime(time.strptime(task[0]))
        print("You're working on {} {} for".format(task[2] if task[2] else "task", "[{}]".format(task[1]) if task[1] else "") + helper.parseTime(timepassed))

def stop():
    cursor.execute("SELECT * FROM status")
    task = cursor.fetchone()
    if not task:
        print("You aren't currently working on a task. Use horologium start to start working.")
    else:
        timepassed = time.time() - time.mktime(time.strptime(task[0]))
        cursor.execute("INSERT INTO history VALUES (?,?,?,?)", (task[0],task[1],task[2],timepassed))
        print("You were working on {} {} for".format(task[2] if task[2] else "task", "[{}]".format(task[1]) if task[1] else "") + helper.parseTime(timepassed))
    


functions = {"start": start, "status": status, "stop": stop}
functions[args.command]()

db.close()

