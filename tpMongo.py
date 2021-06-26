from pymongo import MongoClient
import json
import requests

client = MongoClient('localhost')

db= client['paises']
coleccion=db['pais']

def conexionUrl(id):
    url = "https://restcountries.eu/rest/v2/callingcode/" + id
    
    resp = requests.get(url)

    if (resp.status_code != 404):

        data = json.loads(resp.content)

        codigoPais = data[0]['callingCodes'][0],
        nombrePais = data[0]['name'],
        capitalPais = data[0]['capital'],
        region = data[0]['region'],
        latitud = data[0]['latlng'][0],
        longitud = data[0]['latlng'][1],

        pais = coleccion.count_documents({
            "codigoPais": codigoPais[0]
        })

        if (pais == 1):
            coleccion.update_one({
                "codigoPais": codigoPais[0]
            },{
                "$set": {
                    "codigoPais": codigoPais[0],
                    "nombrePais": nombrePais[0],
                    "capitalPais": capitalPais[0],
                    "region": region[0],
                    "latitud": latitud[0],
                    "longitud": longitud[0],
                }
            })
        else: 
            coleccion.insert_one({
                "codigoPais": codigoPais[0],
                "nombrePais": nombrePais[0],
                "capitalPais": capitalPais[0],
                "region": region[0],
                "latitud": latitud[0],
                "longitud": longitud[0],
            }) 

for i in range(301):
    if (i == 300):
        print("Carga Completada")
    else: 
        conexionUrl(str(i))