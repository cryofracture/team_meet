import os
import json
from flask import Flask, jsonify, abort, request, Response
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
local_data = os.environ['TEAM_FILE']


app = Flask(__name__)

# team_file = os.environ['TEAM_FILE']
# team_file = json.load(open(Path("dock_mongo/data/support-eng.json")))

class CreateTeamMember:
    def __init__(self, team_member, city, country, email):
        api_url = tzdb_url + f"/v2.1/get-time-zone?key={tzdb_api_key}&format=json&by=zone&zone={country}/{city}"
        tz = requests.get(api_url).json()

        self.name = str(team_member.capitalize())
        self.utc_offset = get_utc_offset(tz['gmtOffset'])
        self.abbrevation = tz['abbreviation']
        self.timezone = tz['zoneName']
        self.email = email

    def returnNewMember(self):
        return CreateTeamMember()

def get_utc_offset(gmtOffset):
    hour = 60
    minute = 60
    utc_offset = gmtOffset / hour / minute
    return utc_offset
        
def get_tz(city, country):
    city = city.capitalize()
    country = country.capitalize()
    api_url = tzdb_url + f"/v2.1/get-time-zone?key={tzdb_api_key}&format=json&by=zone&zone={country}/{city}"
    print(api_url)

    timezone = requests.get(api_url).json()
    return timezone['']

def load_local_db():
    data = json.load(open(local_data, "r"))
    return data

@app.route('/create-teammember/<string:team_member>', methods=['GET','PUT'])
def create_teammember(team_member):
    city = request.args.get('city').replace(" ","_")
    country = request.args.get('country')
    email = request.args.get('email')
    new_teammember = CreateTeamMember(team_member, city, country, email)
    
    if request.method == "PUT":
        new_teammate = {  "name": new_teammember.name,
                            "utc_offset": new_teammember.utc_offset,
                            "abbreviation": new_teammember.abbrevation,
                            "timezone": new_teammember.timezone.replace("_"," "),
                            "email": new_teammember.email
                        }
        try:
            with open(local_data, mode="r+") as file:
                file.seek(0,2)
                position = file.tell() -1
                file.seek(position)
                file.write( ",{}]".format(json.dump(new_teammate), indent=4))
            return(jsonify({"success": f"{team_member} added."}))
        except:
            return(print("Error."))
    elif request.method == "GET":
        return_payload = {  "name": new_teammember.name,
                            "utc_offset": new_teammember.utc_offset,
                            "abbreviation": new_teammember.abbrevation,
                            "timezone": new_teammember.timezone.replace("_"," "),
                            "email": new_teammember.email
                        }
        return(jsonify(return_payload))

@app.route("/get-local-time/<string:team_member>", methods=('get', 'post'))
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
