import sys
import requests
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) != 2:          
        print("Length must be 2")
        sys.exit(1)
    url = sys.argv[1]
    if not url.startswith("https"):
        url="https://"+url
    try:
        header={ 'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url,headers=header)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print("Error in finding url:", e)
        sys.exit(1)
    soup = BeautifulSoup(response.text, "html.parser")
    
    if soup.title:
        print(soup.title.get_text(strip=True))
    else:
        print("No title found")

    body = soup.body
    if body:
        body_text = body.get_text(strip=True)
        print(body_text)
    else:
        print("No body content found")
    
    links = soup.find_all("a", href=True)

    if links:
        for link in links:
            print(link['href'])
    else:
        print("No link found.")
if __name__ == "__main__":
    main()

