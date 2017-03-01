#!/usr/bin/python

import sqlite3 as sql
import sys
import io


con = sql.connect('test.db')

with con:

    cur = con.cursor()
    
    counter = int(input("How many students are you entering today? "))
    while counter > 0:
        s_id = int(raw_input("What is the student ID? "))
        s_name = raw_input("What is the student name? ")
        s_major = raw_input("What is the student major? ")
        s_career = raw_input("What is the student career? ")
        params = (s_id, s_name, s_major, s_career)
        cur.execute("INSERT INTO Student VALUES(?,?,?,?)", params)
        con.commit()
        counter = counter -1

    tablecur = cur.execute("SELECT * FROM Student")
    for row in tablecur:
        print "Student ID = ", row[0]
        print "Student Name = ", row[1]
        print "Student Major = ", row[2]
        print "Student Proposed Career = ", row[3]
    
