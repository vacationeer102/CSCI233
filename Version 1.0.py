#!/usr/bin/python

from Tkinter import *
import sqlite3 as sql
import sys
import os
from tabulate import tabulate


def create_file(student, rec_num, eval_num, letter_list):
    for s_row in student:
        student_id= s_row[0]
        student_name= s_row[1]
    student_file= open("%s.txt" % student_id, "w+")
    student_file.write("Student ID \t %s \t Student Name \t %s\n\nNumber of Recommendations\t %s\t Number of Evaulations\t %s\n\n" %(student_id, student_name, rec_num, eval_num))
    student_file.write(tabulate(letter_list, headers=["Professor's Name","Rec or Eval?","Time of Submission","Relationship"]))

class Main_Window(Frame):
    
    def createWidgets(self):
        global rowno
        rowno= 0
        
        self.s_id_l = Label(self, text= "Enter Student ID:")
        self.s_id_l.grid(row= rowno, column= 0)

        self.s_id_e = Entry(self)
        self.s_id_e.grid(row= rowno, column= 1)

        self.s_id_b = Button(self, text= "Search", command= self.search)
        self.s_id_b.grid(row= rowno, column= 2)

        self.QUIT = Button(self, text= "QUIT", command= self.quit)
        self.QUIT.grid(row= rowno, column= 3)

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
            
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
                        
root = Tk()
app = Main_Window(master=root)
app.mainloop()
root.destroy()
