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


def extract_categories_urls():
    aside_parse = BeautifulSoup(page, "html.parser")
    liste = aside_parse.find("div", class_="side_categories")
    categories_titles = []
    categories_url = []
    for li in liste.ul.li.find_all("li"):
        category_title = li.a.text.strip()
        category_url = str(li.a['href'])
        categories_titles.append(category_title)
        categories_url.append(category_url)
        print(category_url)
    return categories_titles, categories_url

def scraping (url_to_work):
    url_to_work = url_to_work
    # print(f"Scraping de la page n°{check_number_pages} de la catégorie {categories_titles[page_number_category]}")
    print(f"url = {url_to_work}")
    reponse = requests.get(url_to_work)
    page_to_work = reponse.content
    soup = BeautifulSoup(page_to_work, "html.parser")
    articles = soup.find_all("article") # Cibler chaque article
    scraped_books = []
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
        note = notation[rating[-1]] # Conversion int
        image_url = soup.find("img").get("src")
        image_name = requests.get("http://books.toscrape.com" + image_url[5:]).content
        image_filename = os.path.join("images", os.path.basename(book_title.text + ".jpg"))
        image_clean_filename = re.sub(r"[^a-zA-z0-9-.]", "", image_filename)
        with open(image_clean_filename, "wb") as img_file:
            img_file.write(image_name)
        ligne = [clean_url, upc.text, book_title.text, price_excl_tax, price_incl_tax, stock, book_description, category, note, str("http://books.toscrape.com" + image_url[5:])]
        scraped_books.append(ligne)
    return scraped_books

def csv_create(datas_path, category_url):
    check_number_pages = 1
    fichier_csv = open(datas_path, "a", encoding="utf-8", newline="")
    en_tete = ["URL Produit", "Code UPC", "Titre", "Prix TTC", "Prix HT", "Stock Disponible", "Description", "Catégorie", "Note", "URL Image"]
    writer = csv.writer(fichier_csv, delimiter=";")
    writer.writerow(en_tete)
    url_to_work = "http://books.toscrape.com/catalogue/" + str(category_url)[:-10] + "page-" + str(check_number_pages) + ".html"
    multipage = requests.get(url_to_work)
    return multipage, writer, fichier_csv, check_number_pages

def browse_urls(categories_urls):
    for index, category_url in enumerate(categories_urls):
        datas_path = os.path.join("datas", f"{categories_titles[index]}.csv")
        multipage, writer, fichier_csv, check_number_pages = csv_create(datas_path, category_url)
        if "404" in str(multipage):
            scraped = scraping("http://books.toscrape.com/catalogue/" + str(category_url)[:-10] + "index.html")
            writer.writerows(scraped)
            fichier_csv.close()
        else:
            while "404" not in str(multipage):
                url_to_work = "http://books.toscrape.com/catalogue/" + str(category_url)[:-10] + "page-" + str(check_number_pages) + ".html"
                multipage = requests.get(url_to_work)
                if "404" in str(multipage):
                    print(f"Pas de page {check_number_pages}. Catégorie {category_url} terminée.")
                    break
                scraped = scraping("http://books.toscrape.com/catalogue/" + str(category_url)[:-10] + "page-" + str(check_number_pages) + ".html")
                writer.writerows(scraped)
                check_number_pages += 1
            fichier_csv.close()

if __name__ == "__main__":
    categories_titles, categories_urls = extract_categories_urls()
    browse_urls(categories_urls)