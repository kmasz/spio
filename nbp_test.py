import json
from urllib import request
import pandas as pd
import sqlite3


nbp_link = 'http://api.nbp.pl/api/exchangerates/rates/a/usd/?format=json'

def main():
    data = request.urlopen(nbp_link)
    data = data.read().decode("utf-8")
    data = json.loads(data)
    data = pd.DataFrame(data)
    data = data['rates'].to_json()
    data = json.loads(data)
    data = pd.DataFrame(data)
    #print(data)
    dzien = data.iat[0, 0]
    wartosc = data.iat[1, 0]
    print(data.iat[0, 0])
    print(data.iat[1, 0])
    conn = sqlite3.connect('currency.db')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS usd_pln(id INTEGER PRIMARY KEY, date TEXT, value REAL)")
    c.execute("INSERT INTO usd_pln (date, value) VALUES (?, ?)",
              (dzien, wartosc))
    conn.commit()
    c.close()
    conn.close()



    conn.close()
    conn2 = sqlite3.connect('currency.db')
    usd_price = pd.read_sql("SELECT * FROM usd_pln ORDER BY 1 DESC LIMIT 1", conn2)
    conn2.close()
    price = float(usd_price['value'])
    current_date = usd_price['date'][0]
    print(current_date)




if __name__ == '__main__': main()
