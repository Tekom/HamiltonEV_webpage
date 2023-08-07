from django.shortcuts import render
import pyrebase

config = {
    "apiKey": "AIzaSyCXoxYJ14-8THiRHs3VAM7KYNKnLEqhkMk",
    "authDomain": "hamiltonhv-database.firebaseapp.com",
    "projectId": "hamiltonhv-database",
    "databaseURL": "https://hamiltonhv-database-default-rtdb.firebaseio.com/",
    "storageBucket": "hamiltonhv-database.appspot.com",
    "messagingSenderId": "1048401158234",
    "appId": "1:1048401158234:web:69af507d7af92aff357863",
    "measurementId": "G-F0E516TF2X"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def home(request):
    data = {'test':'graph'}
    return render(request, 'telemetria/index.html', context=data)