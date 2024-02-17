# Firstname Lastname
# MCS 275 Project 4
# This project was adapted from [source] and I am the sole author of the
# changes except as noted in README.md.

import flask
import sqlite3


# Create Flask (application) object
app = flask.Flask("Gradebook")

@app.route("/")
def front_page():
    """Front page which displays and gives options to the users about what they want to do"""
    return """<!doctype html>
                <html>
                <head>
                <title>
                    Gradebook
                </title>
                <style>
                    ul li a {
                    display: inline-block;
                    background-color: #4CAF50; /* set button color to green */
                    color: white;
                    font-size: 18px;
                    padding: 8px 16px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-bottom: 10px;
                    }
                    ul li a:hover {
                    background-color: #2d5d2f; /* set button color to darker shade of green on hover */
                    }
                </style>

                </head>
                <body>
                    <h1>Choose action</h1>
                    <ul>
                    <li><a href="/edit">Edit Grades</a></li>
                    <li><a href="/students">View Grades</a></li>
                    <li><a href="/input">Input Grades</a></li>
                    </ul>
                </body>
                </html>
                 """


@app.route("/edit")
def edit_grades():
    """Displays the list of assignment names"""
    #establishing connection to the database
    conn = sqlite3.connect('gradebook.sqlite')
    cursor = conn.cursor()

    # Query the database for the names of all columns except student_name'
    cursor.execute("PRAGMA table_info(grades)")
    #Retrieving all the data
    columns = cursor.fetchall()
    #Getting the names of the assignment in a list
    column_names = [column[1] for column in columns[2:]]

    # Close the database connection
    conn.close()

    return flask.render_template("listassignments.html", columns=column_names)


#The next function implements the /input route and is adapted from
#https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/bugreport/bugreport.py
@app.route("/edit/<assignment_name>", methods=["GET", "POST"])
def show_edit_column(assignment_name):
    """Displays the list of the student names and a text box by them in which they can edit the grades"""

    if flask.request.method == "GET":
        #Establishing connection with the database
        conn = sqlite3.connect('gradebook.sqlite')
        cursor = conn.cursor()

        # Query the database for all grades of the selected assignment name
        cursor.execute(f"SELECT student_name, {assignment_name} FROM grades")
        rows = cursor.fetchall()

        # Close the database connection
        conn.close()

        return flask.render_template("editgrades.html", column=assignment_name, grades=rows)
    else:  
         #If the request.method = "POST"
           
        # Get the form data
        grades = [(name, flask.request.form[name]) for name in flask.request.form]

        # Connect to the database
        conn = sqlite3.connect('gradebook.sqlite')
        cursor = conn.cursor()

        # Update the grades in the database
        for grade in grades:
            cursor.execute(f"UPDATE grades SET {assignment_name} = ? WHERE student_name = ?", (grade[1], grade[0]))

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Redirect to the page (/edit/done)
        return flask.redirect("/edit/done")





@app.route("/edit/done")
def edit_grade_completed():
    "Tell the user the action was completed"
    return """<!doctype html>
    <html>
    <head>
    <title>Gradebook: Grade edited</title>
    <style>
        body {
            background-color: #f0f0f0;
        }
        h1 {
            color: #444;
            text-align: center;
            margin-top: 50px;
        }
        p {
            font-size: 18px;
            text-align: center;
            margin-top: 20px;
        }
        ul {
            list-style-type: none;
            text-align: center;
            margin-top: 30px;
        }
        li {
            display: inline-block;
            margin-right: 20px;
        }
        a {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 5px;
            background-color: #4CAF50;
            color: #fff;
            text-decoration: none;
        }
        
    </style>
    </head>
    <body>
        <h1>Done</h1>
        <p>The grade has been edited. What would you like to do next?</p>
        <ul>
            <li><a href="/edit">Edit another grade</a></li>
            <li><a href="/students">View grades</a></li>
            <li><a href="/input">Input a grade</a></li>
        </ul>
    </body>
    </html>
"""

#The next function implements the /input route and is adapted from
#https://github.com/daviddumas/mcs275spring2023/blob/main/samplecode/html/bugreport/bugreport.py
@app.route('/input', methods=['GET', 'POST'])
def input_grades():
    """Displaying textboxes where the user can input the name of the grades and the grades of the students"""
    if flask.request.method == "GET":
        # Display list of students for all grades
        conn = sqlite3.connect('gradebook.sqlite')
        cursor = conn.cursor()
        cur = cursor.execute('SELECT student_name FROM grades')
        students = cur.fetchall()
        names = []
        #Storing the studentnames as a list in names
        for stu in students:
            names.append(stu[0])

        return flask.render_template('inputgrades.html', students=names)
    
    else:
        #IF the request.method == POST
        #Connecting to the database
        conn = sqlite3.connect('gradebook.sqlite')
        cursor = conn.cursor()
        #Getting the name of the assignment which was entered by the user
        new_grade_name = flask.request.form["grade_name"]
        #Adding that assignment name as a new column
        cursor.execute(f"ALTER TABLE grades ADD COLUMN {new_grade_name} INTEGER;")

        #Getting the grades of the students
        for name in flask.request.form:
            grade = flask.request.form[name]

            # Update the grade for the current student and assignment name
            cursor.execute(f"UPDATE grades SET {new_grade_name} = ? WHERE student_name = ?", (grade, name))
        conn.commit()
        conn.close()
        return flask.redirect("/input/done")
    
@app.route("/input/done")
def input_grade_completed():
    "Tell the user the action was completed"
    return """<!doctype html>
    <html>
    <head>
    <title>Gradebook: Grade added</title>
    <style>
        body {
            background-color: #f0f0f0;
        }
        h1 {
            color: #444;
            text-align: center;
            margin-top: 50px;
        }
        p {
            font-size: 18px;
            text-align: center;
            margin-top: 20px;
        }
        ul {
            list-style-type: none;
            text-align: center;
            margin-top: 30px;
        }
        li {
            display: inline-block;
            margin-right: 20px;
        }
        a {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 5px;
            background-color: #4CAF50;
            color: #fff;
            text-decoration: none;
        }
        
    </style>
    </head>
    <body>
        <h1>Done</h1>
        <p>The grade has been added. What would you like to do next?</p>
        <ul>
            <li><a href="/edit">Edit another grade</a></li>
            <li><a href="/students">View grades</a></li>
            <li><a href="/input">Input a grade</a></li>
        </ul>
    </body>
    </html>
"""



@app.route("/students")
def edit_grade():
    """Displays the names of the students and lets user to click on it"""
    conn = sqlite3.connect('gradebook.sqlite')
    cursor = conn.cursor()

    # Query the database for every student's name
    cursor.execute("SELECT student_name FROM grades")
    rows = cursor.fetchall()

    # Store the names in a list
    names = [row[0] for row in rows]

    # Close the database connection
    conn.close()
    return flask.render_template("Names.html", names=names)


@app.route("/students/<name>")
def show_student_grades(name):
    """Displays all the grades of the student the user clicked on"""
    conn = sqlite3.connect('gradebook.sqlite')
    cursor = conn.cursor()

    # Query the database for the student's grades
    cursor.execute('SELECT * FROM grades LIMIT 0')

    # Querry to get all the column names
    header = [description[0] for description in cursor.description]
    final_header = header[2:]

    #Query to get all the grades of the particular student
    cursor.execute("SELECT * FROM grades WHERE student_name = ?", (name,))
    grades = cursor.fetchone()
    final_grades = grades[2:]

    # Close the database connection
    conn.close()

    # Convert the grades tuple to a list of (assignment, grade) pairs
    grade_pairs = list(zip(final_header, final_grades))

    return flask.render_template("showgrades.html", name=name, grades=grade_pairs)
    

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)