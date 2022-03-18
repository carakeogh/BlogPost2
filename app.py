from pyexpat.errors import messages
from urllib import request
import sqlite3
from flask import Flask, render_template, request, g, redirect, url_for
app = Flask(__name__)

@app.route("/")
def main():
    return render_template("base.html")

def get_message_db():
    #open connection to database message_db in g attribute
    if 'message_db' not in g:
        g.message_db = sqlite3.connect("messages.sqlite")

    #create an empty table for the messages
    cmd = \
        'CREATE TABLE IF NOT EXISTS messages (id INT, handle TINYTEXT, message TINYTEXT)'
    g.message_db.execute(cmd)

    return g.message_db


def insert_message(request):
    #get the user-input message and name/handle
    message = request.form['message']        
    handle = request.form['handle']
        
    datab = get_message_db()
    c = datab.cursor()
    error = None

    if error is None:
        c.execute('SELECT * FROM messages')
        
        #create an ID number for each message
        id = len(c.fetchall())+1
        
        #insert the name/handle, message, and ID as a new rew into the table messages
        c.execute(
            'INSERT INTO messages (id, handle, message) VALUES (?, ?, ?)', (id, handle, message)
            )
        
        #commit the connection to the database
        datab.commit()

        return redirect(url_for('main'))

    #close the connection to the database
    datab = g.pop('message_db', None)
    if datab is not None:
        datab.close()

    return render_template('base.html')


@app.route('/submit/', methods=['POST', 'GET'])
def submit_template():
    if request.method == 'GET':
        return render_template('submit.html')
    else:
        #inserts the user's information into the messages table
        message = request.form["message"]
        handle = request.form["handle"]
        insert_message(request)
        return render_template('submit.html')


        
def random_messages(n):
    datab = get_message_db()
    c = datab.cursor()

    #get n random messages from the database
    cmd = 'SELECT * FROM messages ORDER BY RANDOM() LIMIT ?'
    submissions = c.execute(cmd, (n,))
    submissions = c.fetchall()

    datab = g.pop('message_db', None)
    if datab is not None:
        datab.close()

    return submissions


@app.route('/view/')
def view():
    #return five random messages
    r = random_messages(5)
    return render_template('view.html', datab = r)

