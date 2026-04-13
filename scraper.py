import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.com/news"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    headlines = soup.find_all(["h1", "h2", "h3"])
    
    news_list = []
    
    for headline in headlines:
        text = headline.get_text().strip()
        if text:
            news_list.append(text)
    
    print("\nTop Headlines:\n")
    
    for i, news in enumerate(news_list[:15], 1):  # limit 15
        print(f"{i}. {news}")
    
    with open("headlines.txt", "w", encoding="utf-8") as file:
        for news in news_list:
            file.write(news + "\n")
    
    print("\nSaved successfully!")

else:
    print("Failed to fetch website")