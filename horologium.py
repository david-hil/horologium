#!/usr/bin/env python3
import argparse
import sqlite3
import os.path
import time
import helper

parser = argparse.ArgumentParser(description="A simple time stamp clock for the command line")
parser.add_argument("command", help="the command that will be executed", choices=['start','stop', 'status', 'log','report'])
parser.add_argument("-l", "--label", help="the label of the task you're working on (use this for categories like \"Work\")")
parser.add_argument('-t', '--task', help="the task you're working on (use this as a specific description like \"Finishing feature x\")")
group = parser.add_mutually_exclusive_group()
group.add_argument("-n", '--number', help="how many of the last tasks horologium log or report show", type=int)
group.add_argument("-d", '--days', help="how many days back in time horologium log or report show", type=int)


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
        print("There is already a task running. For more info, use horologium status")
        return
    cursor.execute("INSERT INTO status VALUES (?,?,?)", (time.time(), args.label, args.task))
    print("Started time measurement for {}{}.".format(args.task if args.task else "task", " [{}]".format(args.label) if args.label else ""))
    cursor.execute
    db.commit()

def status():
    cursor.execute("SELECT * FROM status")
    task = cursor.fetchone()
    if not task:
        print("There is no task running. Use horologium start to start a task.")
    else:
        timepassed = time.time() - task[0]
        print("You're working on " + helper.parseTask(task) + "for" + helper.parseTime(timepassed))

def stop():
    cursor.execute("SELECT * FROM status")
    task = cursor.fetchone()
    if not task:
        print("There is no task running. Use horologium start to start a task.")
    else:
        timepassed = time.time() - task[0]
        cursor.execute("INSERT INTO history VALUES (?,?,?,?)", (task[0],task[1],task[2],timepassed))
        db.commit()
        cursor.execute("DELETE FROM status WHERE 1=1")
        db.commit()
        print("Stopped time for " + helper.parseTask(task) + " after" + helper.parseTime(timepassed))

def log():
    if args.number:
        cursor.execute("SELECT * FROM history ORDER BY date DESC LIMIT ?", str(args.number))
        rows = cursor.fetchall()
        for task in rows:
            print("On " + time.asctime(time.localtime(task[0])) + " you worked for " + helper.parseTime(task[3]) + " on " + helper.parseTask(task))
    elif args.days:
        cursor.execute("SELECT * FROM history WHERE date > ?", [str(time.time()-86400*args.days)])
        rows = cursor.fetchall()
        for task in rows:
            print("On " + time.asctime(time.localtime(task[0])) + " you worked for " + helper.parseTime(task[3]) + " on " + helper.parseTask(task))
    else:
        cursor.execute("SELECT * FROM history ORDER BY date DESC LIMIT ?", str(5))
        rows = cursor.fetchall()
        for task in rows:
            print("On " + time.asctime(time.localtime(task[0])) + " you worked for " + helper.parseTime(task[3]) + " on " + helper.parseTask(task))

def report():
    if args.days and not (args.label or args.task):
        cursor.execute("SELECT total(time) FROM history WHERE date > ?", [str(helper.timeDaysAgo(args.days))])
        worktime = cursor.fetchone()[0]
        print("You worked in total for" + helper.parseTime(worktime) + " in the last {} days".format(args.days))
        cursor.execute("SELECT DISTINCT label FROM history WHERE date > ?", [str(helper.timeDaysAgo(args.days))])
        labels = cursor.fetchall()
        for label in labels:
            if label[0] is not None:
                cursor.execute("SELECT total(time) FROM HISTORY WHERE label= ? AND date > ?", (str(label[0]), str(helper.timeDaysAgo(args.days))))
                worktime = cursor.fetchone()[0]
                print(("[{}]\t:".format(label[0])) +helper.parseTime(worktime) if len(label[0]) > 5 else ("[{}]\t\t:".format(label[0])) +helper.parseTime(worktime))
    if args.label and args.days and not args.task:
        cursor.execute("SELECT total(time) FROM history WHERE label = ? AND date > ?", (args.label,helper.timeDaysAgo(args.days)))
        worktime = cursor.fetchone()[0]
        print("You worked in total for" + helper.parseTime(worktime) + " on [{}] in the last {} days".format(args.label, args.days))
        cursor.execute("SELECT DISTINCT task FROM history WHERE label = ? AND date > ?", (args.label, str(helper.timeDaysAgo(args.days))))
        tasks = cursor.fetchall()
        for task in tasks:
            if task[0] is not None:
                cursor.execute("SELECT total(time) FROM HISTORY WHERE task= ? AND date > ?", (str(task[0]), str(helper.timeDaysAgo(args.days))))
                worktime = cursor.fetchone()[0]
                print(("{}\t:".format(task[0])) +helper.parseTime(worktime) if len(task[0]) > 5 else ("[{}]\t\t:".format(task[0])) +helper.parseTime(worktime))
    if args.task and args.days and not args.label:
        cursor.execute("SELECT total(time) FROM HISTORY WHERE task= ? AND date > ?", (str(args.task), str(helper.timeDaysAgo(args.days))))
        worktime = cursor.fetchone()[0]
        print("You worked in total for {} on {} in the last {} days".format(helper.parseTime(worktime), args.task, args.days))
    if args.task and args.label and args.days:
        cursor.execute("SELECT total(time) FROM history WHERE label = ? AND task = ? AND date > ?", (args.label, args.task, helper.timeDaysAgo(args.days)))
        worktime = cursor.fetchone()[0]
        print("You worked in total for {} on {} [{}] in the last {} days".format(helper.parseTime(worktime), args.task, args.label, args.days))
    if args.task and args.label and not args.days:
        cursor.execute("SELECT total(time) FROM history WHERE label = ? AND task = ?", (args.label, args.task))
        worktime = cursor.fetchone()[0]
        print("You worked in total for {} on {} [{}]".format(helper.parseTime(worktime), args.task, args.label))
    if args.label and not args.task and not args.days:
        cursor.execute("SELECT total(time) FROM history WHERE label = ?", (args.label,))
        worktime = cursor.fetchone()[0]
        print("You worked in total for" + helper.parseTime(worktime) + " on [{}]".format(args.label))
        cursor.execute("SELECT DISTINCT task FROM history WHERE label = ?", (args.label, ))
        tasks = cursor.fetchall()
        for task in tasks:
            if task[0] is not None:
                cursor.execute("SELECT total(time) FROM HISTORY WHERE task= ?", (str(task[0]),))
                worktime = cursor.fetchone()[0]
                print(("{}\t:".format(task[0])) +helper.parseTime(worktime) if len(task[0]) > 5 else ("[{}]\t\t:".format(task[0])) +helper.parseTime(worktime))
    if args.task and not args.days and not args.label:
        cursor.execute("SELECT total(time) FROM HISTORY WHERE task= ?", (str(args.task),))
        worktime = cursor.fetchone()[0]
        print("You worked in total for {} on {}".format(helper.parseTime(worktime), args.task))        



functions = {"start": start, "status": status, "stop": stop, "log" : log, "report": report}
functions[args.command]()

db.close()

