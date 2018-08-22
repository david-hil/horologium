

# horologium
A simple time stamp clock for the command line
## Usage
### Start
Horologium lets you tack the time you spend on a task. To start tracking time for a task use `horologium start -t "You're Task"`.
You can also add a label to group your tasks into categories.
`horologium start -t "You're Task" -l "a label"`
Labels and tasks are optional, but one of both is required.

### Status
To check whether horologium is currently running or to see how long you have been working, run `horologium status`.

### Stop
To stop horologium after you finished, call `horologium stop`

### Log
To see your last completed tasks, run `horologium log` with either `--days n` to show the tasks of the last n days or `--number n` toshow the last n tasks.

### Report
Use `horologium report` for a summary of what you spent your time on. You can use report with any combination of `-d`, `-l` and `-t`.
`horologium report -l "Work" -d 5` for instance will show you every task with the label "Work" you worked on in the last 5 days, and the total time you worked on tasks with the label "Work" in the last 5 days.
