# Gradebook


## Description
This is a Python Flask application that provides a simple interface to manage student grades in a SQLite database.
The main features of the application are:
(1)  To display a front page where the user can choose if they want to edit grades, input grades, or view grades of the students
(2)  IF the user chooses to edit grades, then they are asked to choose which assingment's grade they want to edit and then they can edit the grades
(3)  If the user chooses to view the grades, they can choose which student's grades they want to view and then that students grades will be displayed
(4) If the user chooses to input a grade, they can write the name of the new assingment and then they can add the grades by the side of the students name

The application uses Flask to handle the requests from the user and it uses Sqlite in the backend to store student's grades. 


## How to test
When a user runs the program, they will have an option to choose if they want to edit the grades, view the grades, or input the grades.

IF the user decides to edit the grades, the program will be redirected to "/edit" where the user will have the option to choose which assignment's grades they want to edit. The user can just click on that assingment and the program will be redirected to "/edit/<assignment_name>" in which the assignment name will be replaced by the name they clicked on. Here the user will be displayed the list of all the students and their current grade in a box and the user can edit that box and they can press save changes when they are done. Then the program will update the database and the program will be redirected to "/edit/done". Here the viewers will be displayed a message that the grade has been edited and the users will also have options if they want to edit another grade, view grades, or input a grade

If the user decides to view grades, the program will be redirected to "/students" where the user will be displayed the list of the students name and the user can click on the name of the student they want to view grades of. After the click on a student's name, the program will be redirected to "/students/<name>" where the name will be replaced by the name of the student. Here, the program will display all the assignments and the grades of that student. If the viewer is done seeing the grades, they can press the back button and go back.

If the viewer decided to view grades, the program will be redirected to "/input" where the user will have the chance to write the name of the new assignment and the input the grades of the assignment by the names of the students. After they are done plugging the grades in, they can hit submit and the program will update the database and a new assignment name and grades according to the user's input. Then the program will be redirected to "/input/done" where the program will display a messae that the grade was added and the users will again have the option about what they want to do next



[What part of the work to create this project was your personal
contribution? Be detailed and specific.  If I can't understand exactly
what you did, as compared to what you adapted from other sources, then
you haven't written enough.]
I have created the whole project by myself including the all the frontend operations in Flask and all the backend querries of Sqlite database. 

