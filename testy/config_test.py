import configparser
config = configparser.ConfigParser()
#zapisyuwnaie do pliku conf
# config['DEFAULT'] = {'ServerType': 'DEV',
#                      'Compresion': 'yes',
#                      'speed': '45'}
# config['TEST'] = {}
# config['TEST']['User'] = 'kmasz'
# config['DANE'] = {}
# dane = config['DANE']
# dane['Port'] = '5432'
# dane['Path'] = 'c:\\program files\\'
#
# with open('example.ini', 'w') as configfile:
#     config.write(configfile)

#odczyt z pliku
config.read('config.ini')
server_type = config['DEFAULT']['servertype']

path = config[server_type]['data_source']
print(path)

if server_type == 'PROD':
    print('PRODUKCJA')
elif server_type == 'DEV':
    print('LOKALNE')
else:
    print('error!')