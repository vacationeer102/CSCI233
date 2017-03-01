#!/usr/bin/python

import sqlite3 as sql
import sys
import io
import datetime


con = sql.connect('test.db')

with con:

    s_cur = con.cursor()
    s_counter = int(input("How many students are you entering today? "))
    while s_counter > 0:
        s_id = int(raw_input("What is the student ID? "))
        s_name = raw_input("What is the student name? ")
        s_major = raw_input("What is the student major? ")
        s_career = raw_input("What is the student career? ")
        params = (s_id, s_name, s_major, s_career)
        s_cur.execute("INSERT INTO Student VALUES(?,?,?,?)", params)
        con.commit()
        s_counter = s_counter -1

    r_e_cur = con.cursor()
    r_e_counter = int(input("Recs/Evals per Day? "))
    while r_e_counter > 0:
        r_e_id = int(raw_input("What is the student ID? "))
        r_e_name = raw_input("What is the recommender name? ")
        r_or_e = str(raw_input("Is this a rec or eval? (r/e) "))
        date_of_submission = datetime.datetime.now()
        r_e_relation = raw_input("What is the recommender's relationship to student? ")
        params = (r_e_id, r_e_name, r_or_e, date_of_submission, r_e_relation)
        r_e_cur.execute("INSERT INTO Recs_Evals VALUES(?,?,?,?,?)", params)
        con.commit()
        r_e_counter = r_e_counter -1

    s_tablecur = s_cur.execute("SELECT * FROM Student")
    for s_row in s_tablecur:
        s_id = s_row[0]
        print "Student ID = ", s_row[0]
        print "Student Name = ", s_row[1]
        print "Student Major = ", s_row[2]
        print "Student Proposed Career = ", s_row[3]
        r_e_tablecur = r_e_cur.execute("SELECT * FROM Recs_Evals WHERE student_ID=?", (s_id,))
        for r_e_row in r_e_tablecur:
            print "Recommender Name = ", r_e_row[1]
            print "Rec or Eval? ", r_e_row[2]
            print "Date of Submission", r_e_row[3]
            print "Relationship to Student = ", r_e_row[4]
            
