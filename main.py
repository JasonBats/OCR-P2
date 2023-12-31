import requests
import csv
from bs4 import BeautifulSoup

# Connexion au site concurrent

url = "http://books.toscrape.com"
reponse = requests.get(url)
page = reponse.content

# Parse du code HTML

soup = BeautifulSoup(page, "html.parser")

articles = soup.find_all("article") # Cibler chaque article

for article in articles:
    h3_elements = article.find_all("h3") # Cibler chaque nom d'article

    for h3 in h3_elements:
        a_elements = h3.find_all("a") # Cibler chaque url d'article

        for a in a_elements:
            url_product = a["href"]
            print("http://books.toscrape.com/" + url_product)
            reponse_product = requests.get("http://books.toscrape.com/" + url_product) # Concatener chaque url
            page_product = reponse_product.content # Ouvrir chaque url
            soup = BeautifulSoup(page_product, "html.parser") # Parser chaque page produit
            tables = soup.find_all("td")
            upc = tables[0]
            book_title = soup.find("h1") # Cibler le titre <h1> de la page
            price_excl_tax = tables[2]
            price_incl_tax = tables[3]
            number_available = tables[5]
            paragraphs = soup.find_all("p")
            book_description = paragraphs[3] # Description = 4ème <p> de la page. Peut mieux faire ?
            ariane = soup.find("ul") # Chercher la liste d'ariane
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
            print(upc.text)
            print(book_title.text)
            print(price_excl_tax.text[1:]) # Slice la devise
            print(price_incl_tax.text[1:])
            print(number_available.text[10:][:-10]) # Pour "In stock (22 available)" Slice les 10 premiers charactères et les 11 derniers pour isoler le nombre
            print(book_description.text)
            print(category.text[1:][:-1]) # Slice les retours à la ligne
            print(note)
            print("http://books.toscrape.com" + image_url[5:])


# Ciblage prix

class_name = "price_color"
prices = soup.find_all("p", class_=class_name)

# Ciblage titres

titles = soup.find_all("h3")

# product_page_urls = []
# for product_url in product_page_urls:
#     product_page_urls.append(product_url.text)


# Alimenter la liste de prix pour chaque prix trouvé

prices_text = []
for price in prices:
    prices_text.append(price.text)

# print(prices_text) # à supprimer

# Alimenter la liste de titres pour chaque titre trouvé

titles_text = []
for title in titles:
    a_tag = title.find("a") #Cibler la balise <a>
    full_title = a_tag["title"] #Rechercher son attribut title et le stocker dans la variable "full_title"
    titles_text.append(full_title) #Alimenter la liste "titles_text" avec les attributs "title" des balises <a> des éléments <h3>

"""   ^^^^^^^^   Pas encore au point !    ^^^^^^^^   """

# print(titles_text)

# FIN VEILLE CONCURRENTIELLE ----------

# Creation fichier CSV

# en_tete = ["titre", "prix"]

# with open("prices.csv", "w", encoding="utf-8") as fichier_csv:
#     writer = csv.writer(fichier_csv, delimiter=",")
#     writer.writerow(en_tete)
#     for title, price in zip(titles, prices):
#         ligne = [title.string, price.string]
#         writer.writerow(ligne) # Commentaire supplémentaire juste pour tester git