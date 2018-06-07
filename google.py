# this is a test to get result from google engine 
import urllib
from bs4 import BeautifulSoup
import requests
import webbrowser

result = []
def google(text):
    text = urllib.parse.quote_plus(text)
    url = 'https://google.com/search?hl=en&q=' + text
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    for g in soup.find_all(class_='g'):
        result.append(g.text)
    return result[0] 
    
print(google("hello world"))        
