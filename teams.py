import requests
import urllib.parse


# Super secret - shhhh
API_TOKEN=""  # Redacted
ENDPOINT_URL="https://www.robotevents.com/api/v2/teams"

teams = [
"690E",
"6660A",
"33631J",
"44310A",
"61666X",
"94300A",
]

division = {
    'Elementary School': 'ES',
    'Middle School': 'MS'
}
query = "&number%5B%5D=".join(teams)

headers = {"Authorization": f"Bearer {API_TOKEN}", "Accept": "application/json"}

buffer = ""
currentPage = 1
while True:
    response = requests.get(f"{ENDPOINT_URL}?&number%5B%5D={query}&program%5B%5D=41&myTeams=false&page={currentPage}", headers=headers)
    json = response.json()
    currentPage = int(json['meta']['current_page'])
    lastPage = int(json['meta']['last_page'])
    for i in range(0, len(json['data'])):
        buffer += f"{json['data'][i]['number']},{division[json['data'][i]['grade']]}\n"
    if currentPage >= lastPage:
        break
    currentPage += 1   # Advance to next page

with open("teams.csv", "w") as file:
    file.write(buffer)

print("Wrote to teams.csv")