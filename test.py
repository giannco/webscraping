import requests
import pandas as pd
import mysql.connector
from bs4 import BeautifulSoup

mydb = mysql.connector.connect(user='root',password='123456',host='localhost', database='testdb', port='3306')

mycursor = mydb.cursor()

#mycursor.execute('TRUNCATE TABLE plays;')
#mydb.commit()

sql = "INSERT INTO plays (hour,animal,dateTransaction,lotteryId) VALUES (%s, %s, %s, %s)" #Lotto activo 1 

daterange = pd.date_range(start='2024-04-09',end='2024-04-28') #Lotto rey
#daterange = pd.date_range(start='13/12/2017', end='30/03/2023') #Lotto activo, granjita

for single_date in daterange:
	
	r = requests.get('https://centrodeapuestaselrey.com.ve/resultados/lotto-activo?date='+single_date.strftime("%d/%m/%Y")) 
	#r = requests.get('https://centrodeapuestaselrey.com.ve/resultados/lotto-rey?date='+single_date.strftime("%d/%m/%Y")) 
	#r = requests.get('https://centrodeapuestaselrey.com.ve/resultados/la-granjita?date='+single_date.strftime("%d/%m/%Y")) 

	soup = BeautifulSoup(r.text, 'lxml')

	div_main = soup.find_all("div", {"class": "row lotery-result-list"})

	print(single_date)
	print(single_date.strftime("%d/%m/%Y"))


	hour = []
	animals = []

	for div in div_main:
		result_time = div.findAll("div", {"class": "hora"})
		result_children= div.findAll("div", {"class": "text"})

		for i in range(result_time.index(result_time[-1])+1):
			val = (pd.to_datetime(result_time[i].get_text()),result_children[i].get_text(),single_date,1)
			mycursor.execute(sql, val)
			mydb.commit()








