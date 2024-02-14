from flask import Flask, request, redirect
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy
from flask.templating import render_template
import datetime
from functools import cmp_to_key

app = Flask(__name__)
app.debug = True

# Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# SQLAlchemy instance
db = SQLAlchemy(app)

migrate = Migrate(app, db)

@app.route('/')
def index():
      # Query all data and then pass it to the template
    tasks = Task.query.all()
    # print(profiles)
    return render_template('index.html', tasks=tasks)



@app.route('/getTasks')
def getTasks():
    tasks = Task.query.all()
    tasks.sort(key=lambda t: t.datetime)
    res = []
    for task in tasks:
        t = {}
        t["id"] = task.id
        t["priority"] = task.priority
        t["task"] = task.task
        t["datetime"] = task.datetime
        t["date"] = str(task.datetime).split(" ")[0]
        t["time"] = getTime(task.datetime)
        t["today"] = False
        if len(res) == 0 or res[len(res)-1][0]["date"] != t["date"]:
            res.append([t])
        else:
            res[len(res)-1].append(t)
    for group in res:
        # group.sort(key=lambda t : t["priority"])
        group.sort(key=cmp_to_key(compare))
        # pri/nt(group[0]["date"])
        if str(group[0]["date"]) == str(datetime.date.today()):
            for i in range(0, len(group)):
                group[i]["today"] = True
    return res

def compare(x, y):
    if x["priority"] < y["priority"]:
        return -1
    elif x["priority"] > y["priority"]:
        return 1
    elif x["datetime"] < y["datetime"]:
        return -1
    elif x["datetime"] < y["datetime"]:
        return 1
    else:
        return 0

def getTime(dt):
    time = str(dt).split(" ")[1].split(":")
    time[0] = int(time[0])
    am = time[0] < 12
    if not am and time[0] != 12:
        time[0] -= 12
    if am and time[0] == 0:
        time[0] = 12
    am = "AM" if am else "PM"
    return "{}:{} {}".format(time[0], time[1], am)
    
# function to add task
@app.route('/addTask', methods=["POST"])
def task():
    # In this function we will input data from the 
    # form page and store it in our database.
    # Remember that inside the get the name should
    # exactly be the same as that in the html
    # input fields
    task = request.form.get("task")
    priority = request.form.get("priority")
    date = request.form.get("date").split('-')
    time = request.form.get("time").split(':')
    if task != '' and priority != '' and date[0] != '' and time[0] != '':
        dt = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), hour=int(time[0]), minute=int(time[1]))
        t = Task(priority=priority, task=task, datetime=dt)
        db.session.add(t)
        db.session.commit()
    return redirect('/')
    # create an object of the Profile class of models
    # and store data as a row in our datatable
    


@app.route('/delete/<int:id>')
def erase(id):
    # Deletes the data on the basis of unique id and 
    # redirects to home page
    data = Task.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')
    
# Models
class Task(db.Model):
    # Id : Field which stores unique id for every row in 
    # database table.
    # first_name: Used to store the first name if the user
    # last_name: Used to store last name of the user
    # Age: Used to store the age of the user
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer, nullable=False)
    task = db.Column(db.String(50), unique=False, nullable=False)
    # date = db.Column(db.Date(), unique=False, nullable=False)
    datetime = db.Column(db.DateTime(), unique=False, nullable=False)
    
    # repr method represents how one object of this datatable
    # will look like
    def __repr__(self):
        return f"Task : {self.task}, Date: {self.date}"

if __name__ == '__main__':
    app.run()