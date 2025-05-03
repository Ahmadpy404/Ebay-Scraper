import asyncio
import aiohttp
import tkinter as tk
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
from openpyxl import Workbook

# --- Async function to fetch product data from eBay ---
async def fetch_product_data(session, ean):
    url = f"https://www.ebay.com/sch/i.html?_nkw={ean}"
    try:
        async with session.get(url) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            listings = soup.select('.s-item')

            if not listings:
                return [ean, "Not Found", "Not Found", "Not Found", "Not Found", "Not Found", "Not Found"]

            listing = listings[0]

            title = listing.select_one('.s-item__title')
            title_text = title.get_text(strip=True) if title else "N/A"

            condition = listing.select_one('.SECONDARY_INFO')
            condition_text = condition.get_text(strip=True) if condition else "N/A"

            price = listing.select_one('.s-item__price')
            price_text = price.get_text(strip=True) if price else "N/A"

            shipping = listing.select_one('.s-item__shipping')
            shipping_text = shipping.get_text(strip=True) if shipping else "N/A"

            location = listing.select_one('.s-item__location')
            location_text = location.get_text(strip=True) if location else "N/A"

            link = listing.select_one('.s-item__link')
            link_href = link['href'] if link else "N/A"

            return [ean, title_text, condition_text, price_text, shipping_text, location_text, link_href]

    except Exception as e:
        return [ean, "Error", str(e), "N/A", "N/A", "N/A", "N/A"]

# --- Run all async tasks ---
async def run_scraper(eans):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_product_data(session, ean) for ean in eans]
        return await asyncio.gather(*tasks)

# --- Save results to Excel ---
def save_to_excel(results):
    wb = Workbook()
    ws = wb.active
    ws.title = "eBay Results"

    headers = ["EAN", "Title", "Condition", "Price", "Shipping", "Location", "Link"]
    ws.append(headers)

    for row in results:
        ws.append(row)

    filename = "eBay_results.xlsx"
    wb.save(filename)
    messagebox.showinfo("Done", f"Results saved to {filename}")

# --- Handle file selection and start process ---
def select_file():
    filepath = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")],
        title="Select EANs TXT File"
    )

    if not filepath:
        return

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            eans = [line.strip() for line in file if line.strip()]
        if not eans:
            messagebox.showerror("Error", "No EANs found in file.")
            return

        messagebox.showinfo("Working", f"Found {len(eans)} EANs. Scraping, please wait...")
        results = asyncio.run(run_scraper(eans))
        save_to_excel(results)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Build the GUI ---
def create_gui():
    root = tk.Tk()
    root.title("eBay EAN Scraper")

    root.geometry("400x200")
    root.configure(bg="#f0f0f0")

    label = tk.Label(root, text="Upload .txt file with EANs (one per line):", bg="#f0f0f0")
    label.pack(pady=20)

    upload_button = tk.Button(root, text="Upload .txt File", command=select_file, width=20, bg="#4caf50", fg="white")
    upload_button.pack()

    root.mainloop()

# --- Run the GUI ---
if __name__ == "__main__":
    create_gui()
