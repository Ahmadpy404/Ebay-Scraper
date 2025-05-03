# 🛒 Ebay Product Scraper

This tool allows you to scrape product details from eBay using a list of EANs (European Article Numbers). It includes a simple graphical user interface (GUI) for ease of use and can be run either from the Python script or as an executable `.exe` file.

---

## 💻 Features

- Upload a `.txt` file containing EANs (one per line)
- Automatically fetch product titles, prices, shipping, and seller info from eBay
- Save results to an Excel (.xlsx) file
- Built-in GUI (no need to use terminal/command-line)

---

## 🧰 Dependencies (for Python `.py` script)

Before running the Python script, install the following packages:

```bash
pip install requests beautifulsoup4 openpyxl tkinter
