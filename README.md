# Employee Database
This is a postgresql database example script that allows the user to add, remove, and update employee data in command prompt (tested only in Windows 10). It also allows the user to view one employee information, or all of the employees information.

This is designed as a project exercise for Grover Gaming's Software Engineer position.

## Installation
Install dependencies with `pip install`:
* `psycopg2`

## Before Running
####Update `conn` to connect to your database
`dbname=` Your database name
`user=` Your username
`host=` Your hostname (or localhost)
`port=` Your port number
`password=` Your password

## Running
Run `python script.py` from the root project directory to run the application.

## Usage
**Add:** Add an employee to the database. Must include employee name, job type, and date of hire (in the form of mm/dd/yyy).\n
**Remove:** Remove an employee from the database.\n
**Update:** Update an existing employee from the database. Able to change employee name, job type, and date of hire (in the form of mm/dd/yyy).\n
**View All:** Shows all of the current employees from the database.\n
**View One:** Shows one of the current employees from the database that is specified.\n


<sup>by Brianna Cappo</sup>
