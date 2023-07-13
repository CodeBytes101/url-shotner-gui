import requests

headers = {
    "Content-type": "application/json",
    "Authorization": "Bearer HDZXieZcFnLtkNHk",
}
id = [88390, 87855, 87854]
for i in id:
    response = requests.delete(f"https://sizl.ink/api/url/{i}/delete", headers=headers)
    print(response)
