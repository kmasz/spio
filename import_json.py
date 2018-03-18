import json
from urllib import request
import pandas as pd
import datetime
import time
import os
import sqlite3

dataLink = 'https://api.coinmarketcap.com/v1/ticker/'
sleep_time = 180 #czas pomiędzy odczytami danych

#c = conn.cursor()
db_data_types = {'24h_volume_usd': 'REAL', 'available_supply': 'REAL', 'id': 'TEXT', 'last_updated': 'REAL',
              'market_cap_usd': 'REAL', 'max_supply': 'REAL', 'name': 'TEXT', 'percent_change_1h': 'REAL',
              'percent_change_24h': 'REAL', 'percent_change_7d': 'REAL', 'price_btc': 'REAL', 'price_usd': 'REAL',
              'rank': 'INTEGER', 'symbol': 'TEXT', 'total_supply': 'REAL'}

def main():

    #TODO dodać inkrementację indexu
    #ids = data[data['id'] == 'bitcoin']




    # TODO dodać obsługe przerwania pętli
    #########################################################
    while True:
        data = request.urlopen(dataLink)
        data = data.read().decode("utf-8")
        data = json.loads(data)
        data = pd.DataFrame(data)
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
    _time = datetime.datetime.fromtimestamp(ts)  #konwersja z linux timestamp na datę
    return _time

def continiousreading(data):
    #TODO dodać sprawdznie czy dane się zmieniły, jeśli nie to nic nie robić
    conn = sqlite3.connect('cryptocurrency.db')
    #datafile = open('db.txt', 'a')
    #datafile.write(_data.to_string())
    #print('Data write down to file db.txt')
    #atafile.close()
    kolumna_danych = data.loc[:, 'id']   #bierzemy z DataFrame tylko kolumnę z 'id'
    print(str(timestamp2time(time.time())) + ' : Zaczynam zapis danych', end=' ')
    for k in range(0,len(kolumna_danych)):  #przechodzimy przez wszystkie zczytane dane -k jest od 0 do długości zmiennej: kolumna_danych
        str_data = data[data['id'] == kolumna_danych[k]]    #czytamy wiersz w którym 'id' równe jest wartości kalumna danych[k]
        nazwa_pliku = str(kolumna_danych[k]) + '.txt'   #tworzymy zmienną string o nazwie zawartej w zmiennej kolumna_danych[k]
        datafile = open(nazwa_pliku, 'a')   #otwieramy plik o nazwie zawartej w kolumna_danych[k]
        table_name = str(kolumna_danych[k]) #zminna przechowująca nazwę tabeli
        # c.execute('CREATE TABLE IF NOT EXISTS table_name("24h_volume_usd" REAL, available_supply REAL, id TEXT, last_updated REAL, market_cap_usd REAL, max_supply REAL, name TEXT, percent_change_1h REAL, percent_change_24h REAL, percent_change_7d REAL, price_btc REAL, price_usd REAL, rank INTEGER, symbol TEXT, total_supply REAL)')
        #str_data.drop(axis=0)

        str_data.to_sql(table_name, conn, if_exists='append', index=False, dtype=db_data_types)

        if os.stat(nazwa_pliku).st_size == 0:   #sprawdzmy czy plik jest pusty -jeśli tak to zapisujemy nazwy indeksów, jeśli nie tylko dane
            datafile.write(str_data.to_string() + '\n')
        else:
            datafile.write(str_data.to_string().split('\n')[1] + '\n')
        #print('Data write down to file ', nazwa_pliku)  #pomocnicze drukowanie -do usunięcia
        print('*', end='', flush=True)
        datafile.close()    #zamykamy strumień pliku


    conn.close()
    print('\n' + str(timestamp2time(time.time())) + ' : Dane zapisono. Czekam '+ str(sleep_time) +' sekund')
    time.sleep(sleep_time)  #czekamy 60 sekund


if __name__ == '__main__': main()
