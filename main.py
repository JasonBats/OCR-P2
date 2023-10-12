# VEILLE CONCURRENTIELLE ----------

import requests
import csv
from bs4 import BeautifulSoup

url = "http://books.toscrape.com"
reponse = requests.get(url)
page = reponse.content

soup = BeautifulSoup(page, "html.parser")

class_name = "price_color"
prices = soup.find_all("p", class_=class_name)

prices_text = []
for price in prices:
    prices_text.append(price.text)

print(prices_text)

titles = soup.find_all("h3")

titles_text = []
for title in titles:
    a_tag = title.find("a") #Cibler la balise <a>
    full_title = a_tag["title"] #Rechercher son attribut title et le stocker dans la variable "full_title"
    titles_text.append(full_title) #Alimenter la liste "titles_text" avec les attributs "title" des balises <a> des éléments <h3>

"""   ^^^^^^^^   Pas encore au point !    ^^^^^^^^   """

print(titles_text)

# FIN VEILLE CONCURRENTIELLE ----------

en_tete = ["titre", "prix"]

with open("prices.csv", "w", encoding="utf-8") as fichier_csv:
    writer = csv.writer(fichier_csv, delimiter=",")
    writer.writerow(en_tete)
    for title, price in zip(titles, prices):
        ligne = [title.string, price.string]
        writer.writerow(ligne)