#!/usr/bin/python

from Tkinter import *
import sqlite3 as sql
import sys
import os


class Main_Window(Frame):
    def createWidgets(self):
        self.s_id_l = Label(self, text= "Enter Student ID:")
        self.s_id_l.pack(side= "left")

        self.s_id_e = Entry(self)
        self.s_id_e.pack(side= "left")

        self.s_id_b = Button(self, text= "Search", command= self.search)
        self.s_id_b.pack(side= "left")

        self.QUIT = Button(self, text= "QUIT", command= self.quit)
        self.QUIT.pack(side= "left")

        self.restart = Button(self, text= "RESTART", command= self.restart_program)
        self.restart.pack(side= "left")


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


    def search(self):
        s_id = self.s_id_e.get()
        con = sql.connect('test.db')

        with con:

            s_cur = con.cursor()
            r_e_cur = con.cursor()
            
            s_tablecur = s_cur.execute("SELECT * FROM Student WHERE student_id =?", (s_id,))
            for s_row in s_tablecur:
                student = "Student ID = ", s_row[0], "Student Name = ", s_row[1], "Student Major = ", s_row[2], "Student Proposed Career = ", s_row[3]
                self.student_l = Label(self, text= student)
                self.student_l.pack(expand= 1, side= "bottom")
                
                r_e_temp = r_e_cur.execute("SELECT COUNT(r_e_name) FROM Recs_Evals WHERE r_e_id=?", (s_id,))
                for row in r_e_temp:
                    r_e_size=row[0]

                r_e_tablecur = r_e_cur.execute("SELECT * FROM Recs_Evals WHERE r_e_id=?", (s_id,))
                r_e_list = [[None for y in range(4)] for x in range(r_e_size)]
                i= 0
                for r_e_row in r_e_tablecur:
                    recommender = "Recommender Name = ", r_e_row[1], "Rec or Eval? ", r_e_row[2], "Date of Submission", r_e_row[3], "Relationship to Student = ", r_e_row[4]
                    r_e_list[i][0] = r_e_row[1]
                    r_e_list[i][1] = r_e_row[2]
                    r_e_list[i][2] = r_e_row[3]
                    r_e_list[i][3] = r_e_row[4]
                    i = i+1
                    self.recommender_l = Label(self, text= recommender)
                    self.recommender_l.pack(expand= 1, side= "bottom")

                for j in range (0, len(r_e_list)):
                    print r_e_list[j]

    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
    
root = Tk()
app = Main_Window(master=root)
app.mainloop()
root.destroy()
