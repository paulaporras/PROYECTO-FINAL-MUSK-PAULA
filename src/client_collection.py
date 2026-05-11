import json
import os
import pandas as pd

from src.client import Client
from datetime import datetime

class ClientCollection():
    def __init__(self, clients=None):        
        if clients is None:
            with open("data/clients.json", "r") as f:
                self.clients = json.load(f)
            self.df = pd.DataFrame(self.clients)
        else:
            self.clients = [c.__dict__ for c in clients]
            self.df = pd.DataFrame(self.clients)

    def clean_data(self):
        clients_clean = {c["client_id"]: c for c in self.clients}.values()

        for client in clients_clean:
            
            client["name"] = client["name"].strip()
            client["country"] = client["country"].strip().title()
            try:
                dt = datetime.strptime(str(client["signup_date"]), "%Y-%m-%d")
            except ValueError:
                dt = datetime.fromisoformat(str(client["signup_date"]))
            client["signup_date"] = dt.strftime("%Y-%m-%d")

        self.clients = list(clients_clean)

    def total_clients(self):
        return len(self.clients)

    def sales_csv_size(self):
        return os.path.getsize("data/sales.csv")

    def get_client_by_id(self, id):
        for client_data in self.clients:
            if client_data["client_id"] == id:
                return Client(
                client_id = client_data["client_id"],
                name = client_data["name"],
                country = client_data["country"],
                signup_date = client_data["signup_date"]
                )
        return None
    
    def client_by_country(self, country):
        clients_of_country = []
        
        for client_data in self.clients:
            if client_data["country"] == country.title():
                clients_of_country.append(Client(
                client_id = client_data["client_id"],
                name = client_data["name"],
                country = client_data["country"],
                signup_date = client_data["signup_date"]
                ))
        return clients_of_country