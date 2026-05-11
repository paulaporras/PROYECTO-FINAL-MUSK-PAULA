import pandas as pd

from src.sale import Sale

class SalesCollection():
    def __init__(self, sales = None):
        if sales is None:
            self.df = pd.read_csv("data/sales.csv")
            self.clean_data()
        else:
            self.sales = [s.__dict__ for s in sales]
            self.df = pd.DataFrame(self.sales)
            
    def clean_data(self):

        self.df.dropna(inplace = True)
        self.df.drop_duplicates("sale_id", inplace = True) 

        self.df["product"] = self.df["product"].str.strip()
        self.df["category"] = self.df["category"].str.strip()
        self.df["date"] = pd.to_datetime(self.df["date"])
        self.df["date"] = self.df["date"].dt.strftime("%Y-%m-%d")

    def sales_by_client(self, client_id):
        sales_of_client = []

        sales_of_client_df = self.df[self.df["client_id"] == client_id]

        for _, row in sales_of_client_df.iterrows():
            sales_of_client.append(Sale(
                sale_id = row["sale_id"],
                client_id = row["client_id"],
                product = row["product"],
                category = row["category"],
                amount = row["amount"],
                date = row["date"]
                ))

        return sales_of_client
    
    def total_amount_by_client(self, client_id):
        ventas = self.sales_by_client(client_id)
        total = 0
        for venta in ventas:
            total += venta.amount
        return total

    def total_amount_by_category(self, category):
        ventas_categoria = self.df[self.df["category"] == category]
        total = 0

        for _, row in ventas_categoria.iterrows():
            total += row["amount"]

        return total
    
    def average_sale_by_client(self, client_id):
        ventas = self.sales_by_client(client_id)

        if len(ventas) == 0:
            return 0

        total = self.total_amount_by_client(client_id)
        return total / len(ventas)
        