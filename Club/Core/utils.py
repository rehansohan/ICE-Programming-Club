import requests

def fetch_codeforces_rating(handle):
    if not handle:
        return 0
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    try:
        r = requests.get(url)
        data = r.json()
        if data['status'] == 'OK':
            return data['result'][0].get('rating', 0)
    except:
        return 0

def fetch_codechef_rating(handle):
    if not handle:
        return 0
    url = f"https://competitive-coding-api.herokuapp.com/api/codechef/{handle}"
    try:
        r = requests.get(url)
        data = r.json()
        return data.get('rating', 0)
    except:
        return 0

def fetch_atcoder_rating(handle):
    if not handle:
        return 0
    url = f"https://atcoder-api.herokuapp.com/users/{handle}/history"
    try:
        r = requests.get(url)
        data = r.json()
        if data:
            return data[-1].get('NewRating', 0)
    except:
        return 0
