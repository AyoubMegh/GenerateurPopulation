import concurrent.futures
import requests
import json
import random
from bs4 import BeautifulSoup
from datetime import datetime
from threading import Thread

MAX_THREADS = 30
NOMBRE_PERSONNE_A_GENERER = 10

def genererPersonne():
    person = {}
    output = requests.get("https://fr.fakenamegenerator.com/gen-random-fr-fr.php",headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(output.content,'html.parser')
    person["id"] = random.getrandbits(32)
    person["nin"] = soup.select_one("#details > div.content > div.info > div > div.extra > dl:nth-child(2) > dd > div").previous_sibling
    person["nom"] = soup.select_one("#details > div.content > div.info > div > div.address > h3").string
    person["genre"] = soup.select_one("#details > div.content > div.bcs > div > div:nth-child(1) > img")["alt"]
    person["date_naissance"] = soup.select_one("#details > div.content > div.info > div > div.extra > dl:nth-child(8) > dd").string
    person["age"] = soup.select_one("#details > div.content > div.info > div > div.extra > dl:nth-child(9) > dd").string
    person["zodiac"] = soup.select_one("#details > div.content > div.info > div > div.extra > dl:nth-child(10) > dd").string
    person["groupe_sanguin"] = soup.select_one("#details > div.content > div.info > div > div.extra > dl:nth-child(27) > dd").string
    writeJson(person)

def writeJson(new_data,filename="population.json"):
    with open(filename,'r+',encoding= 'utf8') as file:
        file_data = json.load(file)
        file_data["population"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4,ensure_ascii=False)

def initialiser():
    fichier = { "population" : [] }
    fichier["date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    json_object = json.dumps(fichier, indent = 4)
    with open("population.json", "w") as outfile:
        outfile.write(json_object)

def genererSansThread():
    initialiser()
    for i in range(NOMBRE_PERSONNE_A_GENERER):
        genererPersonne()

genererSansThread()