import requests


def link_shorten(url):
    headers = {
        "Authorization": f"Bearer {'41dd6d539c0cb4b23d427a23ca9f992906073e02'}",
        "Content-Type": "application/json",
    }
    payload = {"long_url": url}
    response = requests.post(
        "https://api-ssl.bitly.com/v4/shorten", json=payload, headers=headers
    )
    print(response.json().get("link"))


link_shorten("https://www.youtube.com/watch?v=ee5aEU4XEnc")
