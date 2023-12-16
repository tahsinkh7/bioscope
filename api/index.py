from flask import Flask, request, Response
import requests
import re

app = Flask(__name__)

@app.route('/<string:channel_id>.m3u8')
def generate_link(channel_id):
    url = channel_id
    headers = {
        "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJmY2IxMjRjYi1iN2VlLTRlZTItOGY4MC01Yzc0ZWFkYTI2NzgiLCJpc3MiOiJIRUlNREFMTCIsInJvbGVzIjpbIlJPTEVfVVNFUiIsIlJPTEVfVVNFUl9BTk9OWU1PVVMiXSwidXNlcm5hbWUiOiJhbm9ueW1vdXMiLCJjbGllbnRfbG9naW5faWQiOjg1NzY4NTkyMDc1LCJjbGllbnRfaWQiOiJkOGYxZjRiNGY5ZjM0YTgxOTZlOWFjN2Y4ZDAyY2ZkNSIsInBsYXRmb3JtX2lkIjoiYzNjOThkMWItYzU4MS00NTJkLWEzODUtOTQxY2E2OTQwMWU5IiwiYm9uZ29faWQiOiJmY2IxMjRjYi1iN2VlLTRlZTItOGY4MC01Yzc0ZWFkYTI2NzgiLCJ1c2VyX3R5cGUiOiJhbm9ueW1vdXMiLCJpYXQiOjE3MDI1NTA1MTMsImV4cCI6MTcxMDMyNjUyMy4wLCJjb3VudHJ5Q29kZSI6IkJEIiwicHJlZmVycmVkX3VzZXJuYW1lIjpudWxsfQ.O3Cx1ooOyf5UibWTYu4S2kAyWafDSAH_6_NF8GL1MprD54UZowRYM1AUxmJ3H2NMWUd6RwLX27Bcoy3B9rui4aH5app-Pp9jiXRMYBluLZ9FJyQ4ZOWFlwv4pUNZ8DLy6Yhwzk6xCVOLGqT1rqqxkC9OMYFn9hNiys19_GOTP3qYSmGzDb3154C3pkTTz8IPOruV0sMRod37ttdR69A7L3ocIG-5Nh2weZY9K8Q3ev3pKEuHv6cblvLn1cDOU_DeRlPpO2D5i6Oht1mjqfUsOiFkT5D4HaeuG2MSj-cc5JjmfeiQ4nMBQZT4ASE0tnMseRo_IiTQV0buZYcF8NWkHL36iJTtlRqFRLaWfRiq8Pqi6h1xA1lsFcX5oYbvS_Q0Qlo1WZrGV6Q4osOhk0lSzNqxcyXKCcfEdO1GEQmjodZIU7DIStifZFiS5WkQyPxMDufpL1VVyI7vBuRKabN4-nZcDEYFNDwN39NgC6N8QQTS9jTd1-Rr3pXH9GSoPSKAVRF1OYxpeNqPar6p65xxWn25EHf6Qqk4xSnkNLuKyytyqPy9cLbjfphF28Ra6wFTNpUZJn0FasTB6ufBDOpcapFJoLlEb7xaB3TAhj8L54QjfVHdhTQchJ99ZS2ONd9y7GWiTOx0wFacox-hXQx16Aw1mPqRiA4FxnQZSecOsMU",
        "referer": "https://gp.bioscopelive.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "country-code": "QkQ%3D"
    }

    response = requests.get(f"https://api3.bioscopelive.com/ironman/api/v1/content/detail/{url}", headers=headers)

    data = response.json()
    link = data["feed"]["source"]["feedLink"]

    amit = "https://edge4.bioscopelive.com/hls/"
    flink = link
    match = re.search(r'\/([^\/]+)\.m3u8$', link)

    if match:
        extracted_part = match.group(1)
        new_url = re.sub(r'\/[^\/]+\.m3u8$', '/' + extracted_part + '.m3u8', link)
        
        # Combine the headers with the new_url
        headers_combined = {
            "authorization": headers["authorization"],
            "referer": headers["referer"],
            "user-agent": headers["user-agent"],
            "Content-Type": headers["Content-Type"],
            "country-code": headers["country-code"]
        }

        # Create a response with a redirect and include headers
        resp = Response("", status=302)
        resp.headers["Location"] = new_url
        resp.headers.update(headers_combined)

        return resp
    else:
        pass

    return ""

@app.route("/ts")
def handle_ts():
    headers = {
        "authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJmY2IxMjRjYi1iN2VlLTRlZTItOGY4MC01Yzc0ZWFkYTI2NzgiLCJpc3MiOiJIRUlNREFMTCIsInJvbGVzIjpbIlJPTEVfVVNFUiIsIlJPTEVfVVNFUl9BTk9OWU1PVVMiXSwidXNlcm5hbWUiOiJhbm9ueW1vdXMiLCJjbGllbnRfbG9naW5faWQiOjg1NzY4NTkyMDc1LCJjbGllbnRfaWQiOiJkOGYxZjRiNGY5ZjM0YTgxOTZlOWFjN2Y4ZDAyY2ZkNSIsInBsYXRmb3JtX2lkIjoiYzNjOThkMWItYzU4MS00NTJkLWEzODUtOTQxY2E2OTQwMWU5IiwiYm9uZ29faWQiOiJmY2IxMjRjYi1iN2VlLTRlZTItOGY4MC01Yzc0ZWFkYTI2NzgiLCJ1c2VyX3R5cGUiOiJhbm9ueW1vdXMiLCJpYXQiOjE3MDI1NTA1MTMsImV4cCI6MTcxMDMyNjUyMy4wLCJjb3VudHJ5Q29kZSI6IkJEIiwicHJlZmVycmVkX3VzZXJuYW1lIjpudWxsfQ.O3Cx1ooOyf5UibWTYu4S2kAyWafDSAH_6_NF8GL1MprD54UZowRYM1AUxmJ3H2NMWUd6RwLX27Bcoy3B9rui4aH5app-Pp9jiXRMYBluLZ9FJyQ4ZOWFlwv4pUNZ8DLy6Yhwzk6xCVOLGqT1rqqxkC9OMYFn9hNiys19_GOTP3qYSmGzDb3154C3pkTTz8IPOruV0sMRod37ttdR69A7L3ocIG-5Nh2weZY9K8Q3ev3pKEuHv6cblvLn1cDOU_DeRlPpO2D5i6Oht1mjqfUsOiFkT5D4HaeuG2MSj-cc5JjmfeiQ4nMBQZT4ASE0tnMseRo_IiTQV0buZYcF8NWkHL36iJTtlRqFRLaWfRiq8Pqi6h1xA1lsFcX5oYbvS_Q0Qlo1WZrGV6Q4osOhk0lSzNqxcyXKCcfEdO1GEQmjodZIU7DIStifZFiS5WkQyPxMDufpL1VVyI7vBuRKabN4-nZcDEYFNDwN39NgC6N8QQTS9jTd1-Rr3pXH9GSoPSKAVRF1OYxpeNqPar6p65xxWn25EHf6Qqk4xSnkNLuKyytyqPy9cLbjfphF28Ra6wFTNpUZJn0FasTB6ufBDOpcapFJoLlEb7xaB3TAhj8L54QjfVHdhTQchJ99ZS2ONd9y7GWiTOx0wFacox-hXQx16Aw1mPqRiA4FxnQZSecOsMU",
        "referer": "https://gp.bioscopelive.com",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
        "country-code": "QkQ%3D"
    }

    ts_id = request.args.get("id")
    base = request.args.get("base")
    response = requests.get(base + ts_id, headers=headers)

    return response.content

if __name__ == '__main__':
    app.run(debug=True)
