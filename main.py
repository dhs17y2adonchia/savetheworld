from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from random import randint
import csv
import os.path

key=os.getenv("key")
app = Flask('')
app.secret_key=bytes(randint(1,10000))

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=["GET"])
def collect_username():
  with open('./data/INFO.txt', 'r') as json_file:
    thisdict = json.load(json_file)
  user = request.args.get("user")
  passw = request.args.get("passw")
  if user == "admin" and passw == "1xxxxx_New" or user == "premier" and passw == "1xxxxx_New":
    print("Hi Owner, I am Social.")
    print("Welcome in, " + user + "!")
    return render_template("adminhomee.html", user=user)
  elif user in thisdict:
    print(user)
    if thisdict[user]== passw:
      return render_template("homee.html")
      print("Welcome in, " + user + "!")
    else:
      return render_template("index.html", failed="This account does not exist!")
  else:  
    return render_template("index.html", failed="This account does not exist!")

#editing
#add methods to app.route and /signup in upload
@app.route('/signup', methods=["GET"])
def collect_data():
  email = request.args.get('email')
  user = request.args.get('user')
  passw = request.args.get('passw')
  with open('./data/INFO.txt', 'r') as json_file:
    thisdict = json.load(json_file)
    if user in thisdict and email in thisdict:
      return render_template("index.html",faileduser="Username taken!", failedemail="Email taken!")
    elif user in thisdict:
      return render_template("index.html",faileduser="Username taken!")
    elif email in thisdict:
      return render_template("index.html",failedemail="Email taken!")
    else:
      thisdict[email] = passw
      thisdict[user] = passw
      with open('./data/INFO.txt', 'w') as json_file:
        json.dump(thisdict, json_file, sort_keys=True)
      return render_template("index.html", success="Account successfully created!")

@app.route('/upload', methods=["GET","POST"])
def collect_hw():
  subjects = request.args.get('subjects')
  hw = request.args.get('hw')
  detailzz = request.args.get('detailzz')
  date = request.args.get('date')

  myData = [[subjects, hw, detailzz, date]]

  csv.register_dialect('myDialect', delimiter=',', quoting=csv.QUOTE_NONE)

  myFile = open('./data/homework.txt', 'a')
  with myFile:
    writer = csv.writer(myFile, dialect='myDialect')
    writer.writerows(myData)
  
###
  # with open('./data/homework.txt') as csvfile:
  #   lastline = (list(csvfile)[x])
  #   print (lastline)
  return render_template("adminhomee.html", aa=subjects, bb=hw, cc=detailzz, dd=date)


    
@app.route('/admin', methods=["GET","POST"])
def go_home():
  # with open('./data/homework.txt') as csv_file:
  #     csv_reader = csv.reader(csv_file, delimiter=',')
  #     line_count = 0
  #     for row in csv_reader:
  #         if line_count == 0:
  #             return(f'Column names are {",".join(row)}')
  #             line_count += 1
  #         else:
  #             print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
  #             line_count += 1
  #     print(f'Processed {line_count} lines.')


  return render_template("upload.html", user="admin")









@app.route('/homee', methods=["GET","POST"])
def homee():
  # with open ("./data/homework.txt", "r") as data_file:
  #   for line in data_file.readlines():
  #       line = line.strip().split()
  #       print (line[0], end=" ")
  #       if line[1] != '0':
  #         print(line[1], end=" ")
  #       if line[2] != '0':
  #         print(line[2], end=" ")
  #       if line[3] != '0':
  #         print(line[3], end=" ")
  return render_template("index.html")


app.run(host='0.0.0.0', port=8080)