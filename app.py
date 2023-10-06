from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

user="bjones"
host="bjones.mysql.database.azure.com"
passwd="Project23!"
database="to_do_list"

# Function to create a database and table if they don't exist
def create_database_table():
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd
    )
    cursor = db.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS ${database}")
    cursor.execute(f"USE ${database}")
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, task VARCHAR(255), status VARCHAR(255))")    
    
    db.close()

# Initialize the database and table
create_database_table()

app = Flask(__name__)

@app.route('/')
def home():
    # Establish a new connection and cursor
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )
    cursor = db.cursor()

    # Execute a SELECT query to fetch tasks and statuses
    cursor.execute("SELECT task, status FROM tasks")

    # Fetch all the rows and store them in a list of dictionaries
    tasks = [{'task': task, 'status': status} for (task, status) in cursor]

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return render_template('index.html', tasks=tasks)
# Write to the database on /add path
@app.route('/add', methods=['POST'])
def add_item():
    task = request.form['task']
    status = request.form['status']

    # Establish a new connection and cursor
    db = mysql.connector.connect(
        host=host,
        user=user,
        passwd=passwd,
        database=database
    )
    cursor = db.cursor()

    cursor.execute("INSERT INTO tasks (task, status) VALUES (%s, %s)", (task, status))
    db.commit()

    cursor.close()  # Close the cursor
    db.close()  # Close the database connection

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run()