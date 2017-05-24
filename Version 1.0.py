#!/usr/bin/python

from Tkinter import *
import sqlite3 as sql
import sys
import os
from tabulate import tabulate
import datetime


def create_file(student, rec_num, eval_num, letter_list):
    for s_row in student:
        student_id= s_row[0]
        student_name= s_row[1]
    student_file= open("%s.txt" % student_id, "w+")
    student_file.write("Student ID \t %s \t Student Name \t %s\n\nNumber of Recommendations\t %s\t Number of Evaulations\t %s\n\n" %(student_id, student_name, rec_num, eval_num))
    student_file.write(tabulate(letter_list, headers=["Professor's Name","Rec or Eval?","Time of Submission","Relationship"]))

class Main_Window(Frame):
    
    def createWidgets(self):
        ##Destroy all previous entries
        for label in self.grid_slaves():
            if int(label.grid_info()["row"]) >= 0:
                label.grid_remove()
        
        self.main_screen = Label(self, text= "Welcome to Student Advising Helper")
        self.main_screen.grid(row= 0, column= 0)

        self.retrieve_button = Button(self, text= "Retrieve Student?", command= self.retrieve)
        self.retrieve_button.grid(row= 1, column= 0)

        self.input_button = Button(self, text= "Input Student?", command= self.s_input)
        self.input_button.grid(row= 2, column= 0)

        self.amend_button = Button(self, text= "Add Recs or Evals?", command= self.amend)
        self.amend_button.grid(row= 3, column= 0)

        self.QUIT = Button(self, text= "QUIT", command= self.quit)
        self.QUIT.grid(row= 4, column= 0)


    def retrieve(self):
        ##Destroy all previous entries
        for label in self.grid_slaves():
            if int(label.grid_info()["row"]) >= 0:
                label.grid_remove()

        global rowno
        rowno= 0
        
        self.s_id_l = Label(self, text= "Enter Student ID:")
        self.s_id_l.grid(row= rowno, column= 0)

        self.s_id_e = Entry(self)
        self.s_id_e.grid(row= rowno, column= 1)

        self.s_id_b = Button(self, text= "Search", command= self.search)
        self.s_id_b.grid(row= rowno, column= 2)

        self.return_menu = Button(self, text= "Return", command= self.createWidgets)
        self.return_menu.grid(row= rowno, column= 3)
        
        self.QUIT = Button(self, text= "QUIT", command= self.quit)
        self.QUIT.grid(row= rowno, column= 4)

        rowno= 1

        global rowno
        

    def blankLabel(self):
        ##Create a blank row
        global rowno
        self.blank = Label(self, text= " ")
        self.blank.grid(row= rowno)
        rowno= rowno+1
        global rowno
        

    def search(self):

        ##Destroy all previous entries
        for label in self.grid_slaves():
            if int(label.grid_info()["row"]) > 0:
                label.grid_remove()

        ##Link to database
        s_id = self.s_id_e.get()
        con = sql.connect('test.db')

        ##Globalize rowno to maintain grid
        global rowno

        self.blankLabel()

        with con:

            ##2 cursors - one for students, one for recommendations
            s_cur = con.cursor()
            r_e_cur = con.cursor()

            ##Create the headings
            self.student_l = Label(self, text= "Student ID")
            self.student_l.grid(row=rowno, column=0)
            self.student_l = Label(self, text= "Student Name")
            self.student_l.grid(row=rowno, column=1)
            self.student_l = Label(self, text= "Proposed Major")
            self.student_l.grid(row=rowno, column=2)
            self.student_l = Label(self, text= "Proposed Career")
            self.student_l.grid(row=rowno, column=3)

            rowno= rowno+1

            ##Print out student information
            s_list = [[None for y in range(5)] for x in range(1)]
            s_tablecur = s_cur.execute("SELECT * FROM Student WHERE student_id =?", (s_id,))
            for s_row in s_tablecur:
                for i in range(len(s_row)):
                    s_list[0][i] = s_row[i]
                    self.student_l = Label(self, text= s_row[i])
                    self.student_l.grid(row= rowno, column= i)
            rowno= rowno+1

            self.blankLabel()

            ##Print out number of recommendations and evaluations
            r_temp = r_e_cur.execute("SELECT COUNT(r_e_name) FROM Recs_Evals WHERE r_e_id=? AND r_or_e= 'r'", (s_id,))
            for row in r_temp:
                r_size= row[0]
                self.recom_amount = Label(self, text= "Number of Recs")
                self.recom_amount.grid(row= rowno, sticky= 'n')

                self.recom_amount = Label(self, text= row[0])
                self.recom_amount.grid(row= rowno, column= 1, sticky= 'n')
            e_temp = r_e_cur.execute("SELECT COUNT(r_e_name) FROM Recs_Evals WHERE r_e_id=? AND r_or_e= 'e'", (s_id,))
            for row in e_temp:
                e_size= row[0]
                self.eval_amount = Label(self, text= "Number of Evals")
                self.eval_amount.grid(row= rowno, column= 2, sticky= 'n')

                self.eval_amount = Label(self, text= row[0])
                self.eval_amount.grid(row= rowno, column= 3, sticky= 'n')
            r_e_size= e_size+r_size
            rowno= rowno+1

            self.blankLabel()

            ##Put the specific details about each recommendation/evaluation into an array
            r_e_tablecur = r_e_cur.execute("SELECT * FROM Recs_Evals WHERE r_e_id=?", (s_id,))
            r_e_list = [[None for y in range(4)] for x in range(r_e_size)]
            i=0
            for r_e_row in r_e_tablecur:
                r_e_list[i][0] = r_e_row[1]
                r_e_list[i][1] = r_e_row[2]
                r_e_list[i][2] = r_e_row[3]
                r_e_list[i][3] = r_e_row[4]
                i=i+1

            ##Print out some headings
            self.recommender_l = Label(self, text= "Professor's Name")
            self.recommender_l.grid(row= rowno, column= 0)

            self.recommender_l = Label(self, text= "Recom? or Eval?")
            self.recommender_l.grid(row= rowno, column= 1)

            self.recommender_l = Label(self, text= "Time of Submission")
            self.recommender_l.grid(row= rowno, column= 2)

            self.recommender_l = Label(self, text= "Relationship")
            self.recommender_l.grid(row= rowno, column= 3)

            rowno= rowno+1

            ##Print out each recommendation/evaulation
            for j in range (len(r_e_list)):
                for k in range (4):
                    self.recommender_l = Label(self, text= r_e_list[j][k])
                    self.recommender_l.grid(row= j+rowno, column= k)

            rowno= rowno+len(r_e_list)

            ##Create a button to make a text file capable of being emailed to student
            self.create_text = Button(self, text= "Create a Text File?", command= lambda: create_file(s_list, r_size, e_size, r_e_list))
            self.create_text.grid(row= rowno)
            

    def s_input(self):
        ##Destroy all previous entries
        for label in self.grid_slaves():
            if int(label.grid_info()["row"]) >= 0:
                label.grid_remove()

        global rowno
        rowno= 0

        self.s_id_l = Label(self, text= "Enter Student ID:")
        self.s_id_l.grid(row= rowno, column= 0)

        self.s_id_e = Entry(self)
        self.s_id_e.grid(row= rowno, column= 1)

        self.s_name_l = Label(self, text= "Enter Student Name:")
        self.s_name_l.grid(row= rowno, column= 2)

        self.s_name_e = Entry(self)
        self.s_name_e.grid(row= rowno, column= 3)

        self.s_major_l = Label(self, text= "Enter Student Major:")
        self.s_major_l.grid(row= rowno, column= 4)

        self.s_major_e = Entry(self)
        self.s_major_e.grid(row= rowno, column= 5)

        self.s_career_l = Label(self, text= "Enter Student Career:")
        self.s_career_l.grid(row= rowno, column= 6)

        self.s_career_e = Entry(self)
        self.s_career_e.grid(row= rowno, column= 7)

        self.enter = Button(self, text= "Done?", command= self.db_student)
        self.enter.grid(row= rowno+1, column= 0)

    def db_student(self):
        s_id = self.s_id_e.get()
        s_name = self.s_name_e.get()
        s_major = self.s_major_e.get()
        s_career = self.s_career_e.get()

        con = sql.connect('test.db')

        with con:
            s_cur= con.cursor()
            s_params = (s_id, s_name, s_major, s_career)
            s_cur.execute("INSERT INTO Student VALUES(?,?,?,?)", s_params)
            con.commit()
        
        ##Destroy all previous entries
        for label in self.grid_slaves():
            if int(label.grid_info()["row"]) >= 0:
                label.grid_remove()

        self.enter = Button(self, text= "Enter Recs?", command= self.amend)
        self.enter.grid(row= 0, column= 0)

        self.return_menu = Button(self, text= "Return", command= self.createWidgets)
        self.return_menu.grid(row= rowno, column= 1)
        
        self.QUIT = Button(self, text= "QUIT", command= self.quit)
        self.QUIT.grid(row= rowno, column= 2)


    def amend(self):
        ##Destroy all previous entries
        for label in self.grid_slaves():
            if int(label.grid_info()["row"]) >= 0:
                label.grid_remove()

        global rowno
        rowno= 0

        self.r_e_id_l = Label(self, text= "Enter Student ID:")
        self.r_e_id_l.grid(row= rowno, column= 0)

        self.r_e_id_e = Entry(self)
        self.r_e_id_e.grid(row= rowno, column= 1)

        self.r_e_name_l = Label(self, text= "Enter Rec Name:")
        self.r_e_name_l.grid(row= rowno, column= 2)

        self.r_e_name_e = Entry(self)
        self.r_e_name_e.grid(row= rowno, column= 3)

        r_e= StringVar()
        options={"r","e"}
        r_e.set("r")

        self.r_or_e_l = Label(self, text= "Rec or eval? (r/e)")
        self.r_or_e_l.grid(row= rowno, column= 4)

        self.r_or_e_e = OptionMenu(self, r_e, *options)
        self.r_or_e_e.grid(row= rowno, column= 5)

        global r_e

        self.r_e_relation_l = Label(self, text= "Enter Rec Relationship:")
        self.r_e_relation_l.grid(row= rowno, column= 6)

        self.r_e_relation_e = Entry(self)
        self.r_e_relation_e.grid(row= rowno, column= 7)

        self.enter = Button(self, text= "Done?", command= self.db_rec)
        self.enter.grid(row= rowno+1, column= 0)


    def db_rec(self):
        r_e_id = self.r_e_id_e.get()
        r_e_name = self.r_e_name_e.get()
        r_or_e = r_e.get()
        r_e_relation = self.r_e_relation_e.get()
        date_of_submission = datetime.datetime.now()

        con = sql.connect('test.db')

        with con:
            r_e_cur= con.cursor()
            r_e_params = (r_e_id, r_e_name, r_or_e, date_of_submission, r_e_relation)
            r_e_cur.execute("INSERT INTO Recs_Evals VALUES(?,?,?,?,?)", r_e_params)
            con.commit()

        
        ##Destroy all previous entries
        for label in self.grid_slaves():
            if int(label.grid_info()["row"]) >= 0:
                label.grid_remove()

        self.enter = Button(self, text= "Enter Recs?", command= self.amend)
        self.enter.grid(row= 0, column= 0)

        self.return_menu = Button(self, text= "Return", command= self.createWidgets)
        self.return_menu.grid(row= rowno, column= 1)
        
        self.QUIT = Button(self, text= "QUIT", command= self.quit)
        self.QUIT.grid(row= rowno, column= 2)

        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
                        
root = Tk()
app = Main_Window(master=root)
app.mainloop()
root.destroy()
