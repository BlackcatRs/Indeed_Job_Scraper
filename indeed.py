#!/usr/bin/env python3

import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs


# Find all of the text between paragraph tags and strip out the html
#page = jobs[0].getText()


# extraire les informations contient des balises div
def extraire_info(job):
    postes = []

    balise_a = job.h2.a

    postes.append( balise_a.get('title'))
    postes.append( job.find('span', 'company').text.strip())
    postes.append( job.find('div', 'recJobLoc').get('data-rc-loc'))
    postes.append( job.find('span', 'date').text.strip())
    postes.append( datetime.today().strftime('%d/%m/%Y'))
    postes.append( 'https://www.indeed.com' + balise_a.get('href'))

    return postes



compteur = 1
jobs_details = []
while True:

    # recuprer la page html et afficher le status de la requete
    url = 'https://fr.indeed.com/emplois?q=technicien%20informatique&l=Paris%20(75)'
    response = requests.get(url)
    print(compteur, "- Resultat de la requete = " + response.reason)

    # cree un objet BeautifulSoup pour analyser le code html recu
    soup = bs(response.text, 'html.parser')

    #recuprer les balises "div" ayant la valeur de class "jobsearch-SerpJobCard unifiedRow
    #row result", type de jobs est <class 'bs4.element.ResultSet'>, accessible sous forme tableau
    jobs = soup.find_all('div', 'jobsearch-SerpJobCard')

    # stocker les information dans un tableau
    for job in jobs:
        jobs_details.append(extraire_info(job))

    # recuprer URL de la page suivante
    try:
        url = 'https://www.indeed.com' \
        + soup.find('a', {'aria-label':'Suivant'}).get('href')
    except:
        break

    #max page web a analyser
    if compteur == 20:
        break
    compteur += 1



# enregistrer dans un csv
with open('jobs.csv', mode='w', newline='', encoding='utf-8') as f:
    jobs_writer = csv.writer(f)

    jobs_writer.writerow(['Intitulé de poste', 'Entreprise', 'Lieu', 'Publié', 'Date', 'JobUrl'])

    for job in jobs_details:
        jobs_writer.writerow(job)





#fin
