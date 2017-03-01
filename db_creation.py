#!/usr/bin/python

import sqlite3 as sql
import sys
import io


con = sql.connect('test.db')

with con:

    cur = con.cursor()
    
    done = int(input("Are you done? 1=y/0=n "))
    while done != "1":
        s_id = int(raw_input("What is the student ID? "))
        s_name = raw_input("What is the student name? ")
        print(s_name)
        s_major = raw_input("What is the student major? ")
        s_career = raw_input("What is the student career? ")
        print(s_id, " ", s_name, " ", s_major, " ", s_career)
        cur.execute("INSERT INTO Student VALUES(s_id, s_name, s_major, s_career)")
        done = int(input("Are you done? 1=y/0=n"))
