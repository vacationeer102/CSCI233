#!/usr/bin/python

from Tkinter import *
import sqlite3 as sql
import sys
import os


class Main_Window(Frame):
    
    def createWidgets(self):
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
            s_tablecur = s_cur.execute("SELECT * FROM Student WHERE student_id =?", (s_id,))
            for s_row in s_tablecur:
                for i in range(len(s_row)):
                    self.student_l = Label(self, text= s_row[i])
                    self.student_l.grid(row= rowno, column= i)
            rowno= rowno+1

            self.blankLabel()

            ##Print out number of recommendations and evaluations
            r_temp = r_e_cur.execute("SELECT COUNT(r_e_name) FROM Recs_Evals WHERE r_e_id=? AND r_or_e= 'r'", (s_id,))
            e_temp = r_e_cur.execute("SELECT COUNT(r_e_name) FROM Recs_Evals WHERE r_e_id=? AND r_or_e= 'e'", (s_id,))
            for row in r_temp:
                r_size= row[0]
                self.recom_amount = Label(self, text= "Number of Recs")
                self.recom_amount.grid(row= rowno, sticky= 'n')

                self.recom_amount = Label(self, text= row[0])
                self.recom_amount.grid(row= rowno, column= 1, sticky= 'n')
            for row in e_temp:
                e_size= row[0]
                self.eval_amount = Label(self, text= "Number of Evals")
                self.eval_amount.grid(row= rowno, column= 2, sticky= 'n')

                self.eval_amount = Label(self, text= row[0])
                self.eval_amount.grid(row= rowno, column= 3, sticky= 'n')
            r_e_size= int(r_size)+int(e_size)
            rowno= rowno+1

            self.blankLabel()

            r_e_tablecur = r_e_cur.execute("SELECT * FROM Recs_Evals WHERE r_e_id=?", (s_id,))
            r_e_list = [[None for y in range(4)] for x in range(r_e_size)]
            i=0
            for r_e_row in r_e_tablecur:
                r_e_list[i][0] = r_e_row[1]
                r_e_list[i][1] = r_e_row[2]
                r_e_list[i][2] = r_e_row[3]
                r_e_list[i][3] = r_e_row[4]
                i=i+1

            self.recommender_l = Label(self, text= "Professor's Name")
            self.recommender_l.grid(row= rowno, column= 0)

            self.recommender_l = Label(self, text= "Recom? or Eval?")
            self.recommender_l.grid(row= rowno, column= 1)

            self.recommender_l = Label(self, text= "Time of Submission")
            self.recommender_l.grid(row= rowno, column= 2)

            self.recommender_l = Label(self, text= "Relationship")
            self.recommender_l.grid(row= rowno, column= 3)

            rowno= rowno+1

            
            for j in range (len(r_e_list)):
                for k in range (4):
                    self.recommender_l = Label(self, text= r_e_list[j][k])
                    self.recommender_l.grid(row= j+rowno, column= k)
                    
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
                        
root = Tk()
app = Main_Window(master=root)
app.mainloop()
root.destroy()
