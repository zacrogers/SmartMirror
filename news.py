from newsapi import NewsApiClient

API_KEY = "d8e099d47f3747f4a3f04e58e73094f6"

def get_nz_headlines():
    try:
        newsapi = NewsApiClient(api_key=API_KEY)
        top_headlines = newsapi.get_top_headlines(category='general', language='en', country='nz')
        articles = top_headlines.get('articles')
        return [article.get('title') for article in articles]
    except:
        return ["NC - No internet connection -  -" for _ in range(5)]

# print(get_nz_headlines())
