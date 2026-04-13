import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import scrolledtext
import webbrowser

# Fetch news function
def fetch_news():
    text_area.delete(1.0, tk.END)

    url = "https://www.bbc.com/news"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("a")

        count = 0

        for article in articles:
            title = article.get_text().strip()
            link = article.get("href")

            if title and link and "/news" in link:
                full_link = "https://www.bbc.com" + link

                # Insert headline
                text_area.insert(tk.END, f"{title}\n", "title")

                # Insert link
                text_area.insert(tk.END, f"{full_link}\n\n", "link")

                count += 1

            if count >= 10:
                break

    else:
        text_area.insert(tk.END, "Failed to fetch news")


# Open link on click
def open_link(event):
    index = text_area.index("@%s,%s" % (event.x, event.y))
    line = text_area.get(index + " linestart", index + " lineend")

    if "http" in line:
        webbrowser.open(line.strip())


# GUI window
root = tk.Tk()
root.title("📰 Live News App")
root.geometry("800x550")
root.configure(bg="#1e1e1e")

# Title label
title_label = tk.Label(
    root,
    text="Live News Headlines",
    font=("Helvetica", 20, "bold"),
    bg="#1e1e1e",
    fg="white"
)
title_label.pack(pady=10)

# Button frame
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=5)

# Fetch button
fetch_btn = tk.Button(
    btn_frame,
    text="Fetch News",
    command=fetch_news,
    bg="#007acc",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=15,
    pady=5,
    relief="flat",
    cursor="hand2"
)
fetch_btn.grid(row=0, column=0, padx=10)

# Clear button
def clear_text():
    text_area.delete(1.0, tk.END)

clear_btn = tk.Button(
    btn_frame,
    text="Clear",
    command=clear_text,
    bg="#444",
    fg="white",
    font=("Arial", 12),
    padx=15,
    pady=5,
    relief="flat",
    cursor="hand2"
)
clear_btn.grid(row=0, column=1, padx=10)

# Text area frame
frame = tk.Frame(root, bg="#1e1e1e")
frame.pack(padx=10, pady=10, fill="both", expand=True)

# Scrollable text area
text_area = scrolledtext.ScrolledText(
    frame,
    wrap=tk.WORD,
    font=("Arial", 11),
    bg="#2d2d2d",
    fg="white",
    insertbackground="white"
)
text_area.pack(fill="both", expand=True)

# Styling tags
text_area.tag_config("title", font=("Arial", 13, "bold"), foreground="#00ffcc")
text_area.tag_config("link", foreground="#4aa3ff", underline=1)

# Bind click
text_area.bind("<Button-1>", open_link)

# Run app
root.mainloop()