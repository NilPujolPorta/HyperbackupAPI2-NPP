from __future__ import barry_as_FLUFL
import json
import time
from os.path import exists
import os

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import selenium
import argparse
import mysql.connector
import yaml
import wget

__version__ ="0.1.1"

def main(args=None):
	ruta = os.path.dirname(os.path.abspath(__file__))
	rutaJson = ruta+"/dadesHyperBackup2.json"
	parser = argparse.ArgumentParser(description='')
	parser.add_argument('-q', '--quiet', help='Nomes mostra els errors i el missatge de acabada per pantalla.', action="store_false")
	parser.add_argument('--json-file', help='La ruta(fitxer inclos) a on es guardara el fitxer de dades json. Per defecte es:'+rutaJson, default=rutaJson, metavar='RUTA')
	parser.add_argument('-g', '--graphicUI', help='Mostra el navegador graficament.', action="store_false")
	parser.add_argument('-v', '--versio', help='Mostra la versio', action='version', version='HyperBackupAPI-NPP v'+__version__)
	args = parser.parse_args(args)
	conf = ruta +"/config/config.yaml"
	if not(os.path.exists(ruta+"/config")):
		os.mkdir(ruta+"/config")
	if not(os.path.exists(ruta+"/errorLogs")):
		os.mkdir(ruta+"/errorLogs")
	if not(os.path.exists(ruta+"/chromedriver.exe")):
		wget.download("https://github.com/NilPujolPorta/HyperbackupAPI2-NPP/blob/master/HyperBackupAPI2/chromedriver.exe?raw=true", ruta+"/chromedriver.exe")
		print()

	if not(exists(conf)):
		print("Emplena el fitxer de configuracio de Base de Dades a config/config.yaml")
		article_info = [
			{
				'BD': {
				'host' : 'localhost',
				'user': 'root',
				'passwd': 'patata'
				}
			}
		]

		with open(conf, 'w') as yamlfile:
			data = yaml.dump(article_info, yamlfile)

	with open(conf, "r") as yamlfile:
		data = yaml.load(yamlfile, Loader=yaml.FullLoader)

	servidor = data[0]['BD']['host']
	usuari = data[0]['BD']['user']
	contrassenya = data[0]['BD']['passwd']

	try:
		mydb =mysql.connector.connect(
			host=servidor,
			user=usuari,
			password=contrassenya,
			database="Hyperbackup2"
			)
		mycursor = mydb.cursor(buffered=True)
		print("Access BDD correcte")
	except:
		try:
			mydb =mysql.connector.connect(
				host=servidor,
				user=usuari,
				password=contrassenya
				)
			print("Base de dades no existeix, creant-la ...")
			mycursor = mydb.cursor(buffered=True)
			mycursor.execute("CREATE DATABASE Hyperbackup2")
			mydb =mysql.connector.connect(
				host=servidor,
				user=usuari,
				password=contrassenya,
				database="Hyperbackup2"
				)
			mycursor = mydb.cursor(buffered=True)
			mycursor.execute("CREATE TABLE credencials (usuari VARCHAR(255), contassenya VARCHAR(255), url VARCHAR(255));")
		except:
			print("Login BDD incorrecte")
			return

	mycursor.execute("SELECT * FROM credencials")
	resultatbd = mycursor.fetchall()
	url = "https://ss0007ns0119.fr3.quickconnect.to/"


	options = Options()
	if args.graphicUI:
		options.headless = True
		options.add_argument('--headless')
		options.add_argument('--disable-gpu')
		options.add_argument('window-size=1720x980')
	browser = webdriver.Chrome(executable_path= ruta+"/chromedriver.exe", options = options)
	for nas in resultatbd:
		browser.get(nas[2])
		time.sleep(10)
		usuari = browser.find_element(by="xpath", value='//*[@id="dsm-user-fieldset"]/div/div/div[1]/input')
		usuari.send_keys(nas[0])
		browser.find_element(by="xpath", value='//*[@id="sds-login-vue-inst"]/div/span/div/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div[3]').click()
		time.sleep(5)
		passwd = browser.find_element(by="xpath", value='//*[@id="dsm-pass-fieldset"]/div[1]/div/div[1]/input')
		passwd.send_keys(nas[1])
		browser.find_element(by="xpath", value='//*[@id="sds-login-vue-inst"]/div/span/div/div[2]/div[2]/div/div[3]/div[2]/div/div[2]/div[4]').click()
		time.sleep(15)
		hypericon=browser.find_element(by="xpath", value='//*[@id="sds-desktop-shortcut"]/div/li[7]')
		hypericon.click()
		time.sleep(10)
		nomsCopies = []
		nomTots = browser.find_elements(by="class name", value="x-tree-node-anchor")
		for nom in nomTots:
			nomsCopies.append(nom.text)
		ultimaCorrecte = []
		statusCopies = []
		roottreenode = browser.find_elements(by="class name", value="x-tree-node")
		y=1
		for treenode in roottreenode:								  #'/html/body/div[11]/div[14]/div[3]/div[1]/div/div/div/div[2]/div[     2    ]/div/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div/div/div
			treenode.click()								      	  #'/html/body/div[11]/div[14]/div[3]/div[1]/div/div/div/div[2]/div[     1    ]/div/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div
			time.sleep(2)									      	  #'/html/body/div[11]/div[14]/div[3]/div[1]/div/div/div/div[2]/div[     2    ]/div/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div
			statusCopies.append(browser.find_element(by="xpath", value='/html/body/div[11]/div[14]/div[3]/div[1]/div/div/div/div[2]/div['+str(y)+']/div/div/div[1]/div/div[2]/div/div/div[1]/div[1]/div').text)
			if ((statusCopies[(y-1)]) != "Eliminando versiones de copia de seguridad...") and ((statusCopies[(y-1)]) !='Deleting backup versions...'):
				ultimaCorrecte.append(browser.find_element(by="xpath", value='/html/body/div[11]/div[14]/div[3]/div[1]/div/div/div/div[2]/div['+str(y)+']/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/span').text)
			                                                            	 #/html/body/div[11]/div[14]/div[3]/div[1]/div/div/div/div[2]/div[     1    ]/div/div/div[1]/div/div[2]/div/div/div[1]/div[2]/div[1]/div[2]/div/div/div[1]/span
			else:
				ultimaCorrecte.append("Es sabra cuan acabi la copia actual")
			y+=1
		
		
		x = 0
		while x < len(nomsCopies):
			print(nomsCopies[x])
			print("Status ultima copia: " + (statusCopies[x]))
			print("Ultima copia correcte: " + (ultimaCorrecte[x]))
			print()
			x+=1

if __name__ =='__main__':
    main()