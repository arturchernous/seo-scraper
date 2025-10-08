import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import os

def scrape_keywords(url):
    try:
        headers = {'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        data = {
            'Element': [],
            'Content': [],
            'Description': []
        }
        
        # Meta keywords
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        if meta_keywords:
            data['Element'].append('Meta Keywords')
            data['Content'].append(meta_keywords.get('content', 'N/A'))
            data['Description'].append('SEO keywords from meta tag')
        
        # Title
        title = soup.find('title')
        if title:
            data['Element'].append('Title')
            data['Content'].append(title.text.strip())
            data['Description'].append('Page title for SEO')
        
        # H1
        h1 = soup.find('h1')
        if h1:
            data['Element'].append('H1')
            data['Content'].append(h1.text.strip())
            data['Description'].append('Main heading')
        
        # H2 (дополнительно, топ 3)
        h2s = soup.find_all('h2')[:3]
        for i, h2 in enumerate(h2s, 1):
            data['Element'].append(f'H2 #{i}')
            data['Content'].append(h2.text.strip())
            data['Description'].append('Subheading')
        
        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            data['Element'].append('Meta Description')
            data['Content'].append(meta_desc.get('content', 'N/A'))
            data['Description'].append('Page summary for search results')
        
        df = pd.DataFrame(data)
        filename = 'seo_report.xlsx'
        df.to_excel(filename, index=False)
        return f"Scraped successfully! Report saved as {filename}\n\n{df.to_string(index=False)}"
    
    except requests.exceptions.RequestException as e:
        return f"Error fetching URL: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"

# GUI
def create_gui():
    root = tk.Tk()
    root.title("SEO Data Scraper Utility")
    root.geometry("600x500")
    root.configure(bg='#f0f0f0')

    # URL Input
    tk.Label(root, text="Enter URL:", bg='#f0f0f0', font=('Arial', 12)).pack(pady=10)
    url_entry = tk.Entry(root, width=60, font=('Arial', 10))
    url_entry.pack(pady=5)
    url_entry.insert(0, "https://example.com")

    # Output Text Area
    output_text = scrolledtext.ScrolledText(root, width=70, height=20, font=('Arial', 10))
    output_text.pack(pady=10)

    # Scrape Button
    def on_scrape():
        url = url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Enter a valid URL!")
            return
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        result = scrape_keywords(url)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)

    scrape_btn = tk.Button(root, text="Scrape Keywords & Generate Report", command=on_scrape,
                           bg='#4CAF50', fg='white', font=('Arial', 12), pady=10, width=30)
    scrape_btn.pack(pady=10)

    # Save Report Button (optional, since auto-saves)
    def save_report():
        if os.path.exists('seo_report.xlsx'):
            filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        else:
            messagebox.showinfo("Info", "Run scrape first!")

    save_btn = tk.Button(root, text="Save Report Manually", command=save_report,
                         bg='#2196F3', fg='white', font=('Arial', 10), pady=5)
    save_btn.pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
