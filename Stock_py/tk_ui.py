# coding=utf-8

from Tkinter import *
import crawler_new
import requests
import webbrowser

class GUIDemo(Frame):
	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.grid()
		self.createWidgets()
		
	def createWidgets(self):
        ####### Input area #######
		self.inputText = Label(self, text = "Input Stock ID:")
		self.inputText.grid(row = 0, column = 0)
		self.inputField = Entry(self, width = 15)
		self.inputField.grid(row = 0, column = 1, columnspan = 1)

		self.inputText1 = Label(self, text = "Expect dividend(default=6.67%):")
		self.inputText1.grid(row = 1, column = 0)
		self.inputField1 = Entry(self, width = 15)
		self.inputField1.grid(row = 1, column = 1, columnspan = 1)

		self.inputText2 = Label(self, text = "Years to calculate(default=5):")
		self.inputText2.grid(row = 2, column = 0)
		self.inputField2 = Entry(self, width = 15)
		self.inputField2.grid(row = 2, column = 1, columnspan = 1)        
         
        ####### Button area #######
		self.new = Button(self, text = "Start!", height = 2, width = 40, command = self.out_text)
		self.new.grid(row = 3, column = 0, columnspan = 2, rowspan = 2)
		####### Output area #######
		self.displayText_p = Label(self, text = None)
		self.displayText_title = Label(self, text = None)
		self.hyperlink = Label(self, text = None)
		self.displayText2 = Label(self, text = None)
		self.displayText3 = Label(self, text = None)
        #self.displayText3.grid()#row=6, column=0, columnspan=2)


	def callback(self, event):
		u_ID = self.inputField.get()
		url_river = "http://goodinfo.tw/StockInfo/ShowK_ChartFlow.asp?RPT_CAT=PER&STOCK_ID=" + u_ID + "&CHT_CAT=WEEK"
		webbrowser.open_new(url_river)

	def clear_previous_msg(self):
		# clear previous data
		self.displayText_title.grid_remove()
		self.hyperlink.grid_remove()
		for i in range(6):
			self.displayText3 = Label(self, text = "               ")
			self.displayText3.grid(row = i + 2, column = 2, columnspan = 1)
			for j in range(1,4):
                # check signed
				self.displayText3 = Label(self, text = "               ")
				self.displayText3.grid(row = i + 2, column = j + 2, columnspan = 1)

				self.displayText_p = Label(self, text = "                                                       ")
				self.displayText_p.grid(row = j + 4, column = 0, columnspan = 2)

		for i in range(len(revenue_topic)):
			self.displayText_fix = Label(self, text = "               ")
			self.displayText_fix.grid(row = 1, column = i+2, columnspan = 1)
	
	def out_text(self):
		global revenue_topic
		revenue_topic = ["年/月", "單月月增", "單月年增", "累積年增"]
		self.clear_previous_msg()

        # import data
		u_ID = self.inputField.get()
		u_Year = self.inputField1.get()
		u_dividend = self.inputField2.get()

		# check input data
		if not self.inputField.get():
			self.displayText_p = Label(self, text = "!!!!!!!Please input stock ID!!!!!!!")
			self.displayText_p.grid(row = 5, column = 0, columnspan = 2)
			return
		if not self.inputField1.get():
			u_Year = "5"
		if not self.inputField2.get():
			u_dividend = "6.67"

		# process basic and second price
		result = crawler_new.start_cal(u_ID, u_Year, u_dividend)

		self.displayText_p = Label(self, text = "Current price: %s" % result["price"][2])
		self.displayText_p.grid(row = 5, column = 0, columnspan = 2)

		self.displayText_p = Label(self, text = "Basic price: %f" % result["price"][0])
		self.displayText_p.grid(row = 6, column = 0, columnspan = 2)

		self.displayText_p = Label(self, text = "Second price: %f" % result["price"][1])
		self.displayText_p.grid(row = 7, column = 0, columnspan = 2)

		# list revenue table
		self.displayText_title = Label(self, text = result["title"])
		self.displayText_title.grid(row = 0, column = 2, columnspan = 4)
		
		for i in range(len(revenue_topic)):
			self.displayText_fix = Label(self, text = revenue_topic[i])
			self.displayText_fix.grid(row = 1, column = i+2, columnspan = 1)		

		for i in range(6):
            # year/month
			self.displayText3 = Label(self, text = result["revenue"][i][0])
			self.displayText3.grid(row = i + 2, column = 2, columnspan = 1)

            # data
			for j in range(1,4):
                # check signed
				if result["revenue"][i][j][0] == "-":
					self.displayText2 = Label(self, text = result["revenue"][i][j])
				else:
					self.displayText2 = Label(self, text = result["revenue"][i][j], bg = "red")
				self.displayText2.grid(row = i + 2, column = j + 2, columnspan = 1)
				
		# 河流圖超連結
		self.hyperlink = Label(self, text = "河流圖在這裡", fg="blue", cursor="hand2")
		self.hyperlink.grid(row = 8, column = 0, columnspan = 2)
		self.hyperlink.bind("<Button-1>", self.callback)
				
if __name__ == '__main__':
    root = Tk()
    app = GUIDemo(master=root)
    app.mainloop()