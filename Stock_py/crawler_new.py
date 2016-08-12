# coding=utf-8

import sys
import lxml
import requests
from bs4 import BeautifulSoup

def get_input_info():
	stock_id = raw_input("Input stock ID: ")
	total_year = raw_input("Input the number of years: ")
	expect_divided = raw_input("Input default divided value: ")

	# collect input into a dictionary and return
	stock_info = {"id":stock_id, "count_year":total_year, "exp_divided":expect_divided}
	return stock_info

def get_url(id):
	# Goodinfo for divided
	payload = {"STOCK_ID":id}
	html_divided = requests.get("http://goodinfo.tw/StockInfo/StockDividendPolicy.asp", params = payload)

	# HiStock for EPR
	Hi_URL = "http://histock.tw/stock/financial.aspx?no="+id+"&t=6"
	html_EPR = requests.get(Hi_URL)

	# Yahoo for EPS, need user-agent headers
	headers_Y = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"}
	Ya_URL = "https://tw.stock.yahoo.com/d/s/company_"+id+".html"
	html_EPS = requests.get(Ya_URL, headers = headers_Y)

	html_t = {"G_divided":html_divided, "H_PER":html_EPR, "Y_EPS":html_EPS}

	return html_t

def get_divided_G(html, count_year, default_divi):
	sum_divided_float = 0.00
	average_divided_float = 0.00
	element_divided = list()
	element_table = list()

	html.encoding = "utf-8"
	soup = BeautifulSoup(html.text,'lxml')
	table = soup.find_all('table', attrs={"class":"solid_1_padding_3_0_tbl", "width":"100%", "border":"0", "cellpadding":"0", "cellspacing":"0", "bgcolor":"#C2CCD3", "style":"font-size:10pt;"})
	
	# sheck stock id valid or not
	#if table:
		#print soup.title.string
	if not table:
		print "Please input correct stock id(G)!"
		sys.exit()

	########## reformat the table ##########

	# get wanted row data(表格內數據) in table
	rows_divided = table[0].find_all("tr", attrs={"align":"center", "height":"23px"})

	# get wanted element(年度與殖利率) into a element_table(list)
	for y in range(int(count_year)):
		element_table = rows_divided[y + 4].find_all("td")
		sum_divided_float += float(element_table[20].string)

	########## end of reformat ##########

	average_divided_float = sum_divided_float / int(default_divi)

	return average_divided_float

def get_PER_H(html):
	element_table = list()
	element_PER = list()

	html.encoding = "utf-8"
	soup = BeautifulSoup(html.text,'lxml')
	table = soup.find_all('table', attrs={"class":"tb-stock tb-outline", "cellspacing":"2"})
	
	# sheck stock id valid or not
	#if table:
		#print soup.title.string
	if not table:
		print "Please input correct stock id!"
		sys.exit()

	########## reformat the table ##########

	rows = table[0].find_all("tr")
	del rows[0]
	
	# get wanted element(本益比) into a element_table(list)
	for item in rows:
		element_table = item.find_all("td", attrs={"style":"width:50px;"})
		
		for i in range(len(item)/2):
			element_PER.append(float(element_table[i].string))
	
	# delete oldest 5 months, total 60 months
	del element_PER[64:45:-5]

	########## end of reformat ##########


	return sum(element_PER) / len(element_PER)

def get_EPS_Y(html):
	element_table = list()
	element_EPS = list()
	element_EPS_data = list()

	#html.encoding = "utf-8"
	soup = BeautifulSoup(html.text,'lxml')
	table = soup.find_all("table", attrs={"width":"630", "border":"0", "cellspacing":"1", "cellpadding":"4"})

	# sheck stock id valid or not
	#if table[0]:
		#print unicode(soup.title.string)
	if not table[0]:
		print "Please input correct stock id!"
		sys.exit()

	########## reformat the table ##########

	rows = table[0].find_all("tr", attrs={"bgcolor":"#FFFFFF"})

	# get first 4 row
	for i in range(len(rows)-1):
		element_table = rows[i].find_all("td", attrs={"align":"center"})
		element_EPS.append(str(element_table[1].string.encode("utf8")))

	# delete 元 in each element
	for i in range(len(element_EPS)):
		element_EPS_data.append(float(element_EPS[i][0:3]))

	########## end of reformat ##########

	return sum(element_EPS_data)

def start_cal(id, year, divided):
	html_dict = get_url(id)
	average_divided = get_divided_G(html_dict["G_divided"], year, divided)
	average_PER = get_PER_H(html_dict["H_PER"])
	sum_EPS = get_EPS_Y(html_dict["Y_EPS"])

	basic_price = 100.00 / float(divided) * average_divided
	second_price = average_PER * sum_EPS
	price = [str(basic_price), str(second_price)]

	print "Basic price: ", price[0]
	print "Second price:", price[1]
	return price

if __name__ == '__main__':
	while True:
		info_stock = get_input_info()
		start_cal(info_stock["id"], info_stock["count_year"], info_stock["exp_divided"])
