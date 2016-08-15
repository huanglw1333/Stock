from Tkinter import *
import crawler_new
import requests

class GUIDemo(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createWidgets()
 
    def createWidgets(self):
        self.inputText = Label(self, text = "Input Stock ID:")
        self.inputText.grid(row = 0, column = 0)
        self.inputField = Entry(self, width = 30)
        self.inputField.grid(row = 0, column = 1, columnspan = 3)
 
        self.inputText1 = Label(self, text = "Expect divided(default=5):")
        self.inputText1.grid(row = 1, column = 0)
        self.inputField1 = Entry(self, width = 30)
        self.inputField1.grid(row = 1, column = 1, columnspan = 3)

        self.inputText2 = Label(self, text = "Years to calculate(default=5):")
        self.inputText2.grid(row = 2, column = 0)
        self.inputField2 = Entry(self, width = 30)
        self.inputField2.grid(row = 2, column = 1, columnspan = 3)        
         
        self.new = Button(self, text = "Start!", height = 2, width = 50, command = self.out_text)
        self.new.grid(row = 4, column = 0, columnspan = 3)

        self.displayText = Label(self, text = "Hello")
        self.displayText.grid(row=5, column=0, columnspan=7)

        self.displayText1 = Label(self, text = "")
        self.displayText1.grid(row=6, column=0, columnspan=7)      

    def out_text(self):   
        # import data
        u_ID = self.inputField.get()
        u_Year = self.inputField1.get()
        u_Divided = self.inputField2.get()

        # check input data
        if not self.inputField.get():
            self.displayText = Label(self, text = "Please input stock ID!!!!!")
            self.displayText.grid(row = 5, column = 0, columnspan = 7)
            return
        if not self.inputField1.get():
            u_Year = "5"
        if not self.inputField2.get():
            u_Divided = "5"

        result = crawler_new.start_cal(u_ID, u_Year, u_Divided)

        self.displayText = Label(self, text = "Basic price: " + result[0])
        self.displayText.grid(row=5, column=0, columnspan=7)

        self.displayText1 = Label(self, text = "Second price: " + result[1])
        self.displayText1.grid(row=6, column=0, columnspan=7)
 
if __name__ == '__main__':
    root = Tk()
    app = GUIDemo(master=root)
    app.mainloop()