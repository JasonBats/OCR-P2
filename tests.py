from bs4 import BeautifulSoup
import requests
import csv

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


while page_number_category < len(categories_url):
    with open(categories_titles[name_category_index]+".csv", "w", encoding="utf-8") as fichier_csv:
        en_tete = ["URL Produit", "Code UPC", "Titre", "Prix TTC", "Prix HT", "Stock Disponible", "Description", "Catégorie", "Note", "URL Image"]
        writer = csv.writer(fichier_csv, delimiter=";")
        writer.writerow(en_tete)
        page_number_category = page_number_category # à vérifier si nécessaire
        check_number_pages = 1
        url_to_work = "http://books.toscrape.com/catalogue/" + str(categories_url[page_number_category])[:-10] + "page-" + str(check_number_pages) + ".html"
        multipage = requests.get(url_to_work)
        print(multipage)
        if "404" in str(multipage):
            url_to_work = "http://books.toscrape.com/catalogue/" + str(categories_url[page_number_category])[:-10] + "index.html"
            print(url_to_work)
            reponse = requests.get(url_to_work)
            page_to_work = reponse.content
            soup = BeautifulSoup(page_to_work, "html.parser")
            articles = soup.find_all("article") # Cibler chaque article
            for article in articles:
                h3_elements = article.find_all("h3") # Dans chaque article, cibler chaque nom d'article
                for h3 in h3_elements:
                    a_elements = h3.find_all("a") # Dans chaque nom d'article, récupérer le lien de l'article
                    for a in a_elements:
                        url_product = a["href"]
                        clean_url = "http://books.toscrape.com/catalogue/" + str(url_product)[9:]
                        reponse_product = requests.get(clean_url) # Concatener chaque url
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
                        ligne = [clean_url, upc.text, book_title.text, price_excl_tax.text[1:], price_incl_tax.text[1:], number_available.text[10:][:-10], book_description.text, category.text[1:][:-1], note, "http://books.toscrape.com" + image_url[5:]]
                        writer.writerow(ligne)
        else:
            while "404" not in str(multipage):
                print("Plusieurs pages")
                url_to_work = "http://books.toscrape.com/catalogue/" + str(categories_url[page_number_category])[:-10] + "page-" + str(check_number_pages) + ".html"
                print(url_to_work)
                multipage = requests.get(url_to_work)
                reponse = requests.get(url_to_work)
                print(reponse)
                if "404" in str(multipage):
                    print("allo ????????????????")
                    break
                page_to_work = reponse.content
                soup = BeautifulSoup(page_to_work, "html.parser")
                articles = soup.find_all("article") # Cibler chaque article
                for article in articles:
                    h3_elements = article.find_all("h3") # Dans chaque article, cibler chaque nom d'article
                    for h3 in h3_elements:
                        a_elements = h3.find_all("a") # Dans chaque nom d'article, récupérer le lien de l'article
                        for a in a_elements:
                            url_product = a["href"]
                            clean_url = "http://books.toscrape.com/catalogue/" + str(url_product)[9:]
                            reponse_product = requests.get(clean_url) # Concatener chaque url
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
                            ligne = [clean_url, upc.text, book_title.text, price_excl_tax.text[1:], price_incl_tax.text[1:], number_available.text[10:][:-10], book_description.text, category.text[1:][:-1], note, "http://books.toscrape.com" + image_url[5:]]
                            writer.writerow(ligne)
                check_number_pages += 1
    page_number_category += 1
    name_category_index += 1


# check_number_pages += 1

