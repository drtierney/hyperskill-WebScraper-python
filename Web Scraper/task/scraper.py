import requests


def scrape_quote(url):
    r = requests.get(url)
    print(r.json().get("content")) if "content" in r.json() and r.status_code == 200 \
        else print("Invalid quote resource!")


user_url = input("Input the URL:\n")
scrape_quote(user_url)
