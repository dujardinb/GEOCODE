import csv
import os.path
class Fichier:
    def __init__(self, path_to_file, separator):
        self.__path_to_file = path_to_file
        self._separator = separator

    @property
    def path_to_file(self):
        return self._path_to_file

    @path_to_file.setter
    def path_to_file(self, path_to_file):
        self._path_to_file = path_to_file

    @property
    def separator(self):
        return self._separator
    @separator.setter
    def separator(self, separator):
        self._separator = separator


    def fileExist(self):
        return  os.path.exists(self.path_to_file)

    def run(self):

        with open(self.path_to_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile,delimiter='\t', quoting=csv.QUOTE_NONE)
            for row in reader:
                print(row['Adresse du lieu 1'], row['CP'], row['Ville'])
