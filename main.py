import requests
import csv
from bs4 import BeautifulSoup

# Connexion au site concurrent

url = "http://books.toscrape.com/catalogue/page-1.html"
reponse = requests.get(url)
page = reponse.content

# Création du CSV + écriture

with open("datas.csv", "w", encoding="utf-8") as fichier_csv:
    en_tete = ["URL Produit", "Code UPC", "Titre", "Prix TTC", "Prix HT", "Stock Disponible", "Description", "Catégorie", "Note", "URL Image"]
    writer = csv.writer(fichier_csv, delimiter=";")
    writer.writerow(en_tete)
    page_number = 1
    while page_number < 5: # Ligne pour tests
    # while reponse != 404: # Tant que l'URL ne renvoie pas de 404 : aller à la page suivante
        url = "http://books.toscrape.com/catalogue/page-" + str(page_number) + ".html" # Ecriture de l'URL de page d'accueil / Actuellement 50 pages
        print(url)
        reponse = requests.get(url)
        page = reponse.content
        soup = BeautifulSoup(page, "html.parser")
        articles = soup.find_all("article") # Cibler chaque article
        for article in articles:
            h3_elements = article.find_all("h3") # Dans chaque article, cibler chaque nom d'article
            for h3 in h3_elements:
                a_elements = h3.find_all("a") # Dans chaque nom d'article, récupérer le lien de l'article
                for a in a_elements:
                    url_product = a["href"]
                    reponse_product = requests.get("http://books.toscrape.com/catalogue/" + url_product) # Concatener chaque url
                    page_product = reponse_product.content # Ouvrir chaque url
                    soup = BeautifulSoup(page_product, "html.parser") # Parser la page produit
                    tables = soup.find_all("td") # Cibler le tableau descriptif de l'article
                    upc = tables[0] # Le code UPC correspond à la 1ère <td> du tableau
                    book_title = soup.find("h1") # Cibler le titre <h1> de la page qui correspond au titre du livre
                    price_excl_tax = tables[2]
                    price_incl_tax = tables[3]
                    number_available = tables[5]
                    paragraphs = soup.find_all("p")
                    book_description = paragraphs[3] # Description = 4ème <p> de la page. Peut mieux faire ?
                    ariane = soup.find("ul") # Chercher la liste  présente dans le fil d'ariane
                    for items in ariane:
                        items = soup.find_all("li")
                        category = items[2] # Récupérer le 3e item de la liste dans le fil d'ariane > Correspond à la catégorie
                    stars = soup.find("p", class_="star-rating") # Trouver le <p> dans lequel se trouvent les étoiles
                    rating = stars.get("class") # Récupérer les noms de classes attribuées aux étoiles
                    match rating[1]: # Isoler le nom de classe correspondant à la note donnée et convertir en int
                        case "One":
                            note = 1
                        case "Two":
                            note = 2
                        case "Three":
                            note = 3
                        case "Four":
                            note = 4
                        case "Five":
                            note = 5
                        case _:
                            note = 0
                    active_item_image = soup.find("img")
                    image_url = active_item_image.get("src")
                            # print("http://books.toscrape.com/" + url_product)
                            # print(upc.text)
                            # print(book_title.text)
                            # print(price_excl_tax.text[1:]) # Slice la devise
                            # print(price_incl_tax.text[1:])
                            # print(number_available.text[10:][:-10]) # Pour "In stock (22 available)" Slice les 10 premiers charactères et les 11 derniers pour isoler le nombre
                            # print(book_description.text)
                            # print(category.text[1:][:-1]) # Slice les retours à la ligne
                            # print(note)
                            # print("http://books.toscrape.com" + image_url[5:])
                    ligne = ["http://books.toscrape.com/catalogue/" + url_product, upc.text, book_title.text, price_excl_tax.text[1:], price_incl_tax.text[1:], number_available.text[10:][:-10], book_description.text, category.text[1:][:-1], note, "http://books.toscrape.com" + image_url[5:]]
                    writer.writerow(ligne)
        page_number += 1


print(reponse)