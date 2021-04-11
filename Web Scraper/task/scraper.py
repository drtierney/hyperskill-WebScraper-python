import requests

file = open("source.html", "wb")
url = input("Input the URL:\n")
r = requests.get(url)
status_code = r.status_code
if status_code == 200:
    file.write(r.content)
    print("Content saved.")
else:
    print(f"The URL returned {status_code}!")

file.close()
