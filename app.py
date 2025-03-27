from flask import Flask, Response
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

app = Flask(__name__)

def fetch_news():
    url = "https://www.tribunaonline.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    articles = soup.find_all("article")  # Ajustar conforme necessário
    news_list = []

    for article in articles:
        title = article.find("h2").text if article.find("h2") else "Sem título"
        link = article.find("a")["href"] if article.find("a") else "#"
        image = article.find("img")["src"] if article.find("img") else ""

        news_list.append({"title": title, "link": link, "image": image})
    
    return news_list

@app.route("/rss")
def generate_rss():
    fg = FeedGenerator()
    fg.title("Tribuna Online - Notícias")
    fg.link(href="https://www.tribunaonline.net/")
    fg.description("Feed RSS personalizado do Tribuna Online")
    
    news_list = fetch_news()
    
    for news in news_list:
        fe = fg.add_entry()
        fe.title(news["title"])
        fe.link(href=news["link"])
        fe.description(f'<img src="{news["image"]}" width="300"/>' if news["image"] else "Sem imagem")
    
    rss_feed = fg.rss_str(pretty=True)
    return Response(rss_feed, mimetype="application/rss+xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
