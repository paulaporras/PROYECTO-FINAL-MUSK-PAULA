import json
import pandas as pd

from src.sales_collection import SalesCollection
from src.client_collection import ClientCollection
from src.functional_utils import *


def generate_report():

    ##### CARGA DE DATOS #####

    sales_collection = SalesCollection()
    client_collection = ClientCollection()

    df_sales = sales_collection.df
    df_clients = client_collection.df

    clientes = df_clients["client_id"].tolist()

    ##### 1. SUMMARY #####

    total_clients = len(df_clients)
    total_sales = len(df_sales)
    total_revenue = df_sales["amount"].sum()

    summary = {
        "total_clients": total_clients,
        "total_sales": total_sales,
        "total_revenue": total_revenue
    }

    ##### 2. CLIENTS #####

    clients = []

    for client in df_clients.to_dict(orient="records"):
        cid = client["client_id"]
        ventas = sales_collection.sales_by_client(cid)
        total_spent = total_amount(ventas)
        sale_count = len(ventas)
        average_sale = round(average_amount(ventas), 2)

        clients.append({
            "client_id": cid,
            "name": client["name"],
            "total_spent": total_spent,
            "sale_count": sale_count,
            "average_sale": average_sale
        })

    ##### 3. TOP CLIENT BY COUNTRY #####

    top_client_by_country = {}

    for country in df_clients["country"].unique():
        df_country = df_clients[df_clients["country"] == country]
        best_client = max(
            df_country["client_id"],
            key=lambda cid: total_amount(sales_collection.sales_by_client(cid))
        )
    
        client_name = df_clients[df_clients["client_id"] == best_client]["name"].values[0]
        top_client_by_country[country] = client_name

    ##### 4. SALES BY CATEGORY #####

    sales_by_category = (
        df_sales.groupby("category")["amount"]
        .sum()
        .to_dict()
    )

    ##### 5. HIGH SPENDING CLIENTS #####

    threshold = 500

    high_spending_clients = [
        df_clients[df_clients["client_id"] == cid]["name"].values[0] 
        for cid in clientes
        if total_amount(sales_collection.sales_by_client(cid)) > threshold
    ]

    ##### 6. MONTHLY SALES #####

    df_sales["date"] = pd.to_datetime(df_sales["date"])
    monthly_sales = (
        df_sales.groupby(df_sales["date"].dt.to_period("M"))["amount"]
        .sum()
        .to_dict()
    )
    monthly_sales = {str(k): v for k, v in monthly_sales.items()}

    ##### JSON FINAL #####
    reporte = {
        "summary": summary,
        "clients": clients,
        "top_client_by_country": top_client_by_country,
        "sales_by_category": sales_by_category,
        "high_spending_clients": high_spending_clients,
        "monthly_sales": monthly_sales
    }
    
    return reporte


if __name__ == "__main__":
    ##### EXPORTAR #####
    reporte = generate_report()
    with open("reporte.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=4, ensure_ascii=False)
    print("Reporte generado correctamente: reporte.json")