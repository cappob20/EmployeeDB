# Created by Brianna Cappo
import psycopg2
import psycopg2.extras
import sys
import time
from psycopg2.errors import InvalidDatetimeFormat

# EDIT THIS BEFORE RUNNING
# sets up connection with databse
conn = psycopg2.connect("dbname='EmployeeDB' user='postgres' host='localhost' port='5433' password='password'")

# get SQL cursor
def getCursor():
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# checks to see if there is a name that already exists
def nameExists(name):
    # with statment will automatically commit
    with conn:
        # with statement will automatically close cursor
        with getCursor() as cur:
            cur.execute("SELECT * FROM employee WHERE name = %s;", (name,))
            if len(cur.fetchall()) == 0:
                return False
            else:
                return True

# retrives the employee name from the databse
def getName():
    name = input("Enter the name of Employee you want to update: ")
    while True:
        if nameExists(name):
            return name
        else:
            print("No employee found with that name.")
            name = input("Enter the name of Employee you want to update: ")

# user can only type mm/dd/yyyy for the date
def inputDate(name):
    doh = input("Enter the Date of hire: ")
    while True:
        try:
            with conn:
                with getCursor() as cur:
                    cur.execute("UPDATE employee SET doh = %s WHERE name = %s;", (doh, name,))
            conn.close()
            break
        except InvalidDatetimeFormat as e:
            print("Sorry, that is an invalid date.")
            doh = input("Enter the Date of hire: ")

# shows one of the current employees from the database that is specified
def viewOne():
    name = input("Enter the name of employee you want to view: ")
    with conn:
        with getCursor() as cur:
            cur.execute("SELECT * FROM employee WHERE name = %s;", (name,))
            for employee in cur.fetchall():
                if name == employee['name']:
                    print(f"Name: {employee['name']} | Job Title: {employee['job_title']} | Date of hire: {employee['doh'].strftime('%m/%d/%Y')}")

# shows all of the current employees from the database
def viewAll():
    with conn:
        with getCursor() as cur:
            cur.execute("SELECT * FROM employee;")
            for employee in cur.fetchall():
                print(f"Name: {employee['name']} | Job Title: {employee['job_title']} | Date of hire: {employee['doh'].strftime('%m/%d/%Y')}")

# update an existing employee from the database
# able to change employee name, job type, and date of hire (in the form of mm/dd/yyy)
def updateEmployee():
    name = getName()
    prompt = input("Please select an option to update: \n 1. Employee Name \n 2. Job Title \n 3. Date of Hire \n")

    if (prompt == "1"):
        update_name = input("Enter the new employee name: ")
        with conn:
            with getCursor() as cur:
                cur.execute(("UPDATE employee SET name = %s WHERE name = %s;"), (update_name, name,))

    if (prompt == "2"):
        job_title = input("Enter the new job title: ")
        with conn:
            with getCursor() as cur:
                cur.execute(("UPDATE employee SET job_title = %s WHERE name = %s;"), (job_title, name,))

    if (prompt == "3"):
        inputDate(name)

    print("Record Updated successfully! \n")
    # print("Returning to main menu... \n")
    # promptUser()

# remove an employee from the database
def removeEmployee():
    name = input("Enter the name of Employee you want to remove: ")
    with conn:
        with getCursor() as cur:
            cur.execute("DELETE FROM employee WHERE name = %s;", (name,))

    print("Employee removed successfully!")

# add an employee to the database
# must include employee name, job type, and date of hire (in the form of mm/dd/yyy)
def addEmployee():
    name = input("Enter employee name: ")
    job_title = input("Enter the job title: ")

    # with statment will automatically commit
    with conn:
        # with statement will automatically close cursor
        with getCursor() as cur:
            cur.execute("INSERT INTO employee (name) VALUES(%s)", (name,))
            cur.execute(("UPDATE employee SET job_title = %s WHERE name = %s;"), (job_title, name,))
    inputDate(name)
    print("Employee added successfully!")

# prompts user in command prompt to choose an option
def promptUser():
    prompt = input("Please select an option: \n 1. Add Employee \n 2. Remove Employee \n 3. Update Existing Employee \n 4. View All Employees \n 5. View One Employee \n 6. Exit \n\n")
    # add
    if (prompt == "1"):
        addEmployee()
    # remove
    if (prompt == "2"):
        removeEmployee()
    # update
    if (prompt == "3"):
        updateEmployee()
    # view all employee information
    if (prompt == "4"):
        viewAll()
    # view one employee information
    if (prompt == "5"):
        viewOne()
    # exits program
    if (prompt == "6"):
        print("Now Exiting...")
        exit()
    time.sleep(2)
    print("\nReturning to main menu... \n")
    time.sleep(2)
    promptUser()

print("\nWelcome to the Employee Database!")
time.sleep(1)
promptUser()
conn.close()
