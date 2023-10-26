from bs4 import BeautifulSoup
import requests
import csv
import os
import re

os.makedirs("images", exist_ok = True)
os.makedirs("datas", exist_ok = True)

url = "http://books.toscrape.com/catalogue/page-1.html"
reponse = requests.get(url)
page = reponse.content

aside_parse = BeautifulSoup(page, "html.parser")
liste = aside_parse.find("div", class_="side_categories")
categories_titles = []
categories_url = []
for li in liste.find_all("li"):
    category_title = li.a.text.strip()
    category_url = str(li.a['href'])
    categories_titles.append(category_title)
    categories_url.append(category_url)

page_number_category = 1 # 1 car 0 = books (catégorie mère)
name_category_index = 1

print(categories_url)

def scraping (url_to_work):
    url_to_work = url_to_work
    print(f"Scraping de la page n°{check_number_pages} de la catégorie {categories_titles[page_number_category]}")
    print(f"url = {url_to_work}")
    reponse = requests.get(url_to_work)
    page_to_work = reponse.content
    soup = BeautifulSoup(page_to_work, "html.parser")
    articles = soup.find_all("article") # Cibler chaque article
    for article in articles:
        url_product = article.h3.a["href"]
        clean_url = "http://books.toscrape.com/catalogue/" + str(url_product)[9:]
        reponse_product = requests.get(clean_url) # Concatener chaque url
        page_product = reponse_product.content # Ouvrir chaque url
        soup = BeautifulSoup(page_product, "html.parser") # Parser la page produit
        tables = soup.find_all("td") # Cibler le tableau descriptif de l'article
        upc = tables[0] # Le code UPC correspond à la 1ère <td> du tableau
        book_title = soup.find("h1") # Cibler le titre <h1> de la page qui correspond au titre du livre
        price_excl_tax = re.sub(r'[^\d.]', '', str(tables[2])) # Récupérer le contenu de la cellule prix, exclure tout ce qui n'est pas un chiffre ou un point
        price_incl_tax = re.sub(r'[^\d.]', '', str(tables[3]))
        stock = re.sub(r'\D', '', str(tables[5]))
        paragraphs = soup.find_all("p")
        book_description = paragraphs[3].text # Description = 4ème <p> de la page. Peut mieux faire ?
        ariane = soup.find("ul") # Chercher la liste  présente dans le fil d'ariane
        category_url = ariane.select_one(":nth-child(3)").a
        category = category_url.text
        rating = soup.find("p", class_="star-rating").get("class") # Trouver le <p> dans lequel se trouvent les étoiles + Récupérer les noms de classes attribuées aux étoiles
        notation = {"One" : 1, "Two" : 2, "Three" : 3, "Four" : 4, "Five" : 5} # Dictionnaire pour équivalence note en str into int
        note = notation[rating[1]] # Conversion int
        image_url = soup.find("img").get("src")
        image_name = requests.get("http://books.toscrape.com" + image_url[5:]).content
        image_filename = os.path.join("images", os.path.basename(book_title.text + ".jpg"))
        image_clean_filename = re.sub(r"[^a-zA-z0-9-.]", "", image_filename)
        with open(image_clean_filename, "wb") as img_file:
            img_file.write(image_name)
        ligne = [clean_url, upc.text, book_title.text, price_excl_tax, price_incl_tax, stock, book_description, category, note, str("http://books.toscrape.com" + image_url[5:])]
        # print(book_description)
        writer.writerow(ligne)

while page_number_category < len(categories_url):
    datas_path = os.path.join("datas", f"{categories_titles[name_category_index]}.csv")
    with open(datas_path, "w", encoding="utf-8", newline="") as fichier_csv:
        en_tete = ["URL Produit", "Code UPC", "Titre", "Prix TTC", "Prix HT", "Stock Disponible", "Description", "Catégorie", "Note", "URL Image"]
        writer = csv.writer(fichier_csv, delimiter=";")
        writer.writerow(en_tete)
        check_number_pages = 1
        url_to_work = "http://books.toscrape.com/catalogue/" + str(categories_url[page_number_category])[:-10] + "page-" + str(check_number_pages) + ".html"
        multipage = requests.get(url_to_work)
        if "404" in str(multipage):
            scraping("http://books.toscrape.com/catalogue/" + str(categories_url[page_number_category])[:-10] + "index.html")
        else:
            while "404" not in str(multipage):
                url_to_work = "http://books.toscrape.com/catalogue/" + str(categories_url[page_number_category])[:-10] + "page-" + str(check_number_pages) + ".html"
                multipage = requests.get(url_to_work)
                if "404" in str(multipage):
                    print(f"Pas de page {check_number_pages}. Catégorie {categories_titles[page_number_category]} terminée.")
                    break
                scraping("http://books.toscrape.com/catalogue/" + str(categories_url[page_number_category])[:-10] + "page-" + str(check_number_pages) + ".html")
                check_number_pages += 1
    page_number_category += 1
    name_category_index += 1