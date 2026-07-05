import requests
from bs4 import BeautifulSoup
import pandas as pd
import gspread
import yagmail
from dotenv import load_dotenv
import os

load_dotenv()
sender_email = os.getenv("EMAIL")
app_password = os.getenv("APP_PASSWORD")
url = "https://webscraper.io/test-sites/e-commerce/allinone/computers/laptops"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

products = soup.find_all("div", class_="product-wrapper")
print(f"Found {len(products)} products")

all_products_data = []

for product in products:
    title = product.find("a", class_="title").text.strip()
    price = product.find("h4", class_="price").text.strip()
    reviews = product.find("p", class_="review-count").text.strip()
    
    all_products_data.append({
        "Product": title,
        "Price": price,
        "Reviews": reviews
    })

df = pd.DataFrame(all_products_data)
print(f"Scraped {len(df)} products")
df["Price"] = df["Price"].str.replace(r"[^\d.]", "", regex=True).astype(float)
df["Reviews"] = df["Reviews"].str.extract(r"(\d+)").astype(int)
df = df.drop_duplicates()

average_price = df["Price"].mean()
total_products = len(df)
most_expensive = df.sort_values("Price", ascending=False).iloc[0]
most_reviewed = df.sort_values("Reviews", ascending=False).iloc[0]

print(df.head())
print("Average price:", average_price)
gc = gspread.service_account(filename="sheets_credentials.json")
sheet = gc.open("Test Automation sheet").sheet1  

sheet.clear()
sheet.update([df.columns.tolist()] + df.values.tolist())

print("Data pushed to Google Sheets")
yag = yagmail.SMTP(sender_email, app_password)

report_content = f"""
Laptop Sales Report

Total products analyzed: {total_products}
Average price: ${average_price:.2f}

Most expensive: {most_expensive['Product']} (${most_expensive['Price']:.2f})
Most reviewed: {most_reviewed['Product']} ({most_reviewed['Reviews']} reviews)

Full data has been updated in the Google Sheet.
"""

yag.send(
    to=sender_email,
    subject="Automated Laptop Sales Report",
    contents=report_content
)

print("Report emailed successfully!")
df.to_csv("laptop_sales_cleaned.csv", index=False)
print("Saved laptop_sales_cleaned.csv")