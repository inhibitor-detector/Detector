import requests
import time

if __name__ == "__main__":
    while True:
        time.sleep(5)
        response = requests.get("http://pampero.it.itba.edu.ar:4141")

        if response.status_code == 200:
            print(response.text)
        
        else:
            print('La solicitud no fue exitosa. Codigo de estado: ', response.status_code)