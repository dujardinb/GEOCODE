import csv
import configparser
import Utils
import secret
import googlemaps

class Geocodage:
    def __init__(self, file_ini):
        self.__file_ini = file_ini
        self.run_geocode()


    def run_geocode(self):
        if not(Utils.fileExist(self.__file_ini)):Utils.erreur('fichier de configuration introuvable. ')
        config = configparser.ConfigParser()
        config.read(self.__file_ini)
        nom_fichier = config['DEFAULT']['nomdufichier']
        chemin_du_fichier = config['DEFAULT']['cheminDuFichier']
        chemin_du_fichier_sortie = config['DEFAULT']['cheminDuFichierSortie']
        separateur = config['DEFAULT']['SeparateurDeChamps']
        ya_entete = config['DEFAULT']['Entete']
        adresse_colonnes = config['DEFAULT']['AdresseColonnes'].split(',')
        #        recherche du séparateur
        sep = ''
        if (separateur == "VIRGULE"):
            sep = csv.excel
        elif (separateur == "POINT_VIRGULE"):
            sep = csv.excel
            sep.delimiter = ";"
        elif (separateur == "TABULATION"):
            sep = csv.excel_tab
        else:
            Utils.erreur("Séparateur de champs non trouvé")

        if (chemin_du_fichier[-1] != '/'): chemin_du_fichier = chemin_du_fichier + "/"
        if (chemin_du_fichier_sortie[-1] != '/'): chemin_du_fichier_sortie = chemin_du_fichier_sortie + "/"
        csv_fichier = chemin_du_fichier + nom_fichier
        if (Utils.fileExist(csv_fichier) == False): Utils.erreur('fichier' + csv_fichier + ' introuvable. ')

        # lecture du fichier CSV
        liste_sortie = [] # Fichier a ecrire
        with open(csv_fichier, newline='') as csvfile:
            buffer = csv.reader(csvfile, sep, quotechar='|')
            i=0
            if(ya_entete != 'OUI'): i = 1
            for row in buffer:
                if (i > 0 ):
                    adresse = ''
                    for item in adresse_colonnes:
                        index = Utils.column_number(item)
                        adresse = adresse+ row[index-1] + ' '
                    resultat = self.geocode_adresse(adresse)
                    lat = resultat[0]['geometry']['location']['lat']
                    lng = resultat[0]['geometry']['location']['lat']
                    statut = resultat[0]['geometry']['location_type']
                    formatted_adress = resultat[0]['formatted_address']

                    row.append(lat)
                    row.append(lng)
                    row.append(formatted_adress)
                    row.append(statut)
                else : # cas de l'entete
                    row.append('Lat')
                    row.append('lng')
                    row.append('Adresse Google')
                    row.append('Statut')
                liste_sortie.append(row)
                i=i+1
                if(i>=10):
                    break

        #ecriture du fichier de sortie
        with open(chemin_du_fichier_sortie + 'sortie_' + nom_fichier, 'w', newline='') as csvfile:
            file_sortie = csv.writer(csvfile, delimiter=sep.delimiter, quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for line in liste_sortie:
                print(line)
                file_sortie.writerow(line)
            print("le fichier:",'sortie_' + nom_fichier ,"est disponible à l'emplacement ", chemin_du_fichier_sortie )


    def geocode_adresse(self,adresse):
        gmaps = googlemaps.Client(key=secret.GMAP_API)
        geocode_result = gmaps.geocode(adresse)
        return geocode_result


