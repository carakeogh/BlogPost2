from pyexpat.errors import messages
from urllib import request
import sqlite3
from flask import Flask, render_template, request, g
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("submit.html")


@app.route("/")
def get_message_db():
    #open connection to database message_db in g attribute
    if 'message_db' not in g:
        g.message_db = sqlite3.connect("message_db.sqlite")

    c = g.message_db.cursor()
    
    #create a table messages to store the user's name/handle, message, and an ID number that we will assign
    c.execute("DROP TABLE IF EXISTS messages")
    c.execute('CREATE TABLE messages (id INT, handle TINYTEXT, message TINYTEXT)') 
    
    #close the connection
    c.close()

    return g.message_db


@app.route('/submit/', methods=['POST', 'GET'])
def insert_message(request):
    if request.method == 'POST':
        #get the user-input message and name/handle
        message = request.form['message']
        handle = request.form['handle']
        
        c = get_message_db.cursor()
        
        #create an ID number for each message
        id = len(c.fetchall())
        values = (id+1, handle, message)
        
        #insert the name/handle, message, and ID as a new rew into the table messages
        c.execute('INSERT INTO messages(id, handle, message) VALUES(?, ?, ?)', values)
        
        #commit and close the connection to the database
        c.commit()
        c.close()
    return message, handle


@app.route('/submit/', methods=['POST', 'GET'])
def render_template(request):
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        try:
            #inserts the user's information into the messages table
            insert_message(request)
            #thanks = "Thank you for your submission!"
            #thanks user for submission and renders the submit template with message and handle information
            return render_template('submit.html', message=request.form['message'], handle=request.form['handle'])
        except: 
            return render_template('submit.html')

        
def random_messages(n):
    c = get_message_db.cursor()
    num = str(n)
    c.execute('SELECT * FROM messages ORDER BY RANDOM() LIMIT(?)', num)
    submissions = c.fetchall()
    c.close()
    return submissions


@app.route('/view')
def render_template2():
    r = random_messages(5)
    return render_template('view.html', submissions = r)

