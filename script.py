import psycopg2
import psycopg2.extras
import sys
from psycopg2.errors import InvalidDatetimeFormat

conn = psycopg2.connect("dbname='EmployeeDB' user='postgres' host='localhost' port='5433' password='password'")

def getCursor():
    return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def nameExists(name):
    with conn:
        with getCursor() as cur:
            cur.execute("SELECT * FROM employee WHERE name = %s;", (name,))
            if len(cur.fetchall()) == 0:
                return False
            else:
                return True

def getName():
    name = input("Enter the name of Employee you want to update: ")
    while True:
        if nameExists(name):
            return name
        else:
            print("No employee found with that name. ")
            name = input("Enter the name of Employee you want to update: ")


def inputDate(name):
    doh = input("Enter the hire date: ")
    while True:
        try:
            with conn:
                with getCursor() as cur:
                    cur.execute("UPDATE employee SET doh = %s WHERE name = %s;", (doh, name,))
            conn.close()
            break
        except InvalidDatetimeFormat as e:
            print("Sorry, that is an invalid date. ")
            doh = input("Enter the hire date: ")

def viewOne():
    name = input("Enter the name of Employee you want to view: ")
    with conn:
        with getCursor() as cur:
            cur.execute("SELECT * FROM employee WHERE name = %s;", (name,))
            print(cur.fetchone())

def viewAll():
    with conn:
        with getCursor() as cur:
            cur.execute("SELECT * FROM employee;")
            print(cur.fetchall())

def updateEmployee():
    name = getName()
    prompt = input("Please select an option to update: \n 1. Name of employee \n 2. Job Title \n 3. Date of hire \n")

    if (prompt == "1"):
        update_name = input("Enter the new name for the Employee: ")
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

    print("Record Updated successfully ")

def removeEmployee():
    name = input("Enter the name of Employee you want to remove: ")
    with conn:
        with getCursor() as cur:
            cur.execute("DELETE FROM employee WHERE name = %s;", (name,))

    print("Employee removed successfully ")

def addEmployee():
    name = input("Enter a name: ")
    job_title = input("Enter the job title: ")

    # with statment will automatically commit
    with conn:
        with getCursor() as cur:
            cur.execute("INSERT INTO employee (name) VALUES(%s)", (name,))
            cur.execute(("UPDATE employee SET job_title = %s WHERE name = %s;"), (job_title, name,))
    inputDate(name)
    print("Employee added successfully ")

def promptUser():
    prompt = input("Please select an option: \n 1. add \n 2. remove \n 3. update \n 4. view all \n 5. view one \n")
    if (prompt == "1"):
        addEmployee()

    if (prompt == "2"):
        removeEmployee()

    if (prompt == "3"):
        updateEmployee()

    if (prompt == "4"):
        viewAll()

    if (prompt == "5"):
        viewOne()
promptUser()
conn.close()
