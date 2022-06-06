import os

#converti une colonne en notation alphabetique et numérique
def column_number(name):
    n = 0
    for c in name:
        n = n * 26 + 1 + ord(c) - ord('A')
    return n

# vérifie si le fichier nom_fichier existe
def fileExist(nom_fichier):
    return os.path.exists(nom_fichier)

#ajoute barre oblique si elle n'existe pas dans le chemin du ficher
def formatPath(path):
    if (path[-1] != '/'): path = path + "/"

def erreur(message):
    print(message)
    quit(1)