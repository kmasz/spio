import json
from urllib import request
import pandas as pd
import datetime
import time
import os

dataLink = 'https://api.coinmarketcap.com/v1/ticker/'

def main():
    data = request.urlopen(dataLink)
    data = data.read().decode("utf-8")
    data = json.loads(data)
    data = pd.DataFrame(data)
    #TODO dodać inkrementację indexu
    #ids = data[data['id'] == 'bitcoin']




    # TODO dodać obsługe przerwania pętli
    #########################################################
    while True:
        continiousreading(data) #nieskończona pętla, która zczytuje dane

    #print(ids['last_updated'][0])
    #czas = datetime.datetime.utcfromtimestamp(int(ids['last_updated'][0]))
    #czas1 = timestamp2time(ids['last_updated'][0])
    #print(czas)
    #print(czas1)


def timestamp2time(ts):
    #jeśli ts nie jest INT to konwertuj na INT
    #TODO dodać obsługe błędu
    if not isinstance(ts,int):
        ts = int(ts)
    _time = datetime.datetime.utcfromtimestamp(ts)  #konwersja z linux timestamp na datę
    return _time

def continiousreading(data):
    #TODO dodać sprawdznie czy dane się zmieniły, jeśli nie to nic nie robić
    #datafile = open('db.txt', 'a')
    #datafile.write(_data.to_string())
    #print('Data write down to file db.txt')
    #atafile.close()
    kolumna_danych = data.loc[:, 'id']   #bierzemy z DataFrame tylko kolumnę z 'id'
    for k in range(0,len(kolumna_danych)):  #przechodzimy przez wszystkie zczytane dane -k jest od 0 do długości zmiennej: kolumna_danych
        str_data = data[data['id'] == kolumna_danych[k]]    #czytamy wiersz w którym 'id' równe jest wartości kalumna danych[k]
        nazwa_pliku = str(kolumna_danych[k]) + '.txt'   #tworzymy zmienną string o nazwie zawartej w zmiennej kolumna_danych[k]
        datafile = open(nazwa_pliku, 'a')   #otwieramy plik o nazwie zawartej w kolumna_danych[k]
        if os.stat(nazwa_pliku).st_size == 0:   #sprawdzmy czy plik jest pusty -jeśli tak to zapisujemy nazwy indeksów, jeśli nie tylko dane
            datafile.write(str_data.to_string() + '\n')
        else:
            datafile.write(str_data.to_string().split('\n')[1] + '\n')
        print('Data write down to file ', nazwa_pliku)  #pomocnicze drukowanie -do usunięcia
        datafile.close()    #zamykamy strumień pliku
    time.sleep(60)  #czekamy 60 sekund



if __name__ == '__main__': main()
