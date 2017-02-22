from Tkinter import *

class Main_Window(Frame):
    def createWidgets(self):
        self.sname_l = Label(self)
        self.sname_l["text"] = "Enter Student Name:"
        self.sname_l.pack({"side":"left"})

        self.sname_e = Entry(self)
        self.sname_e.pack({"side": "left"})

        sname = self.sname_e.get()
        print sname

        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.pack({"side": "left"})


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

root = Tk()
app = Main_Window(master=root)
app.mainloop()
root.destroy()
