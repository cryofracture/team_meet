import os
import json
from flask import Flask, jsonify, abort
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import requests
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials

load_dotenv(find_dotenv())

tzdb_api_key = os.environ['TZDB_API_KEY']
tzdb_url = os.environ['TZDB_URL']


app = Flask(__name__)

# team_file = os.environ['TEAM_FILE']
# team_file = json.load(open(Path("dock_mongo/data/support-eng.json")))

class CreateTeamMember:
    def __init__(self, team_member, city):
        
        

        self.name = str(team_member)
        self.utc_offset = ''
        self.abbrevation = ''
        self.timezone = city
        self.email = ''

        
def get_tz(city, country):
    city = city.capitalize()
    country = country.capitalize()
    api_url = tzdb_url + f"/v2.1/get-time-zone?key={tzdb_api_key}&format=json&by=zone&zone={country}/{city}"
    print(api_url)

    timezone = requests.get(api_url)
    return timezone.text

def load_local_db():
    data = json.load(open("dock_mongo/data/support-eng.json", "r"))
    return data

@app.route("/get-local-time/<string:team_member>")
def get_local_time(team_member):
    data = load_local_db()
    team_member = team_member.capitalize()
    
    teammate_info = [teammate for teammate in data if team_member in teammate['name']]
    
    if teammate_info:
        print(teammate_info)
        print(teammate_info['timezone'])
        api_url = tzdb_url + f"/v2.1/get-time-zone?key={tzdb_api_key}&format=json&by=zone&zone={teammate_info['timezeone']}"
        tzdb_response = requests.get(api_url)
        local_time = tzdb_response['data']['formatted']
        return(jsonify({f"Local time for {team_member}: ": local_time}))
        
    else:
        return(abort(404))


@app.route("/meet/<string:team_member>")
def get_meeting_time(team_member):
    data = load_local_db()
    team_member = team_member.capitalize()
    teammate_info = [teammate for teammate in data if teammate['name'] == team_member]
    if teammate_info:
        return(jsonify({f"info for {team_member}: ": teammate_info}))
    else:
        return(abort(404))
        

if __name__ == "__main__":
    app.run(debug=True)
    # city = "Shanghai"
    # country = "Asia"
    # tz = get_tz(city, country)
    # print(tz)
