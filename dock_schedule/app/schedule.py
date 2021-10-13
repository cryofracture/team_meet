import os
import json
from flask import Flask, jsonify, abort, request
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
        self.utc_offset = "UTC" + str(get_utc_offset(tz['gmtOffset']))
        self.abbrevation = tz['abbreviation']
        self.timezone = tz['zoneName']
        self.email = email

    def returnNewMember(self):
        return CreateTeamMember()

def get_utc_offset(gmtOffset):
    hour = 60
    minute = 60
    utc_offset = int(gmtOffset / hour / minute)
    return utc_offset

def load_local_db():
    data = json.load(open(local_data, "r"))
    return data

@app.route('/create-teammember/<string:team_member>', methods=['GET','PUT','DELETE'])
def create_teammember(team_member):
    city = request.args.get('city')
    country = request.args.get('country')
    email = request.args.get('email')
    args = [city,country,email]
    for arg in args:
        if arg is None:
            return(abort(400))
    new_teammember = CreateTeamMember(team_member, city.replace(" ","_"), country, email)
    
    if request.method == "PUT":
        new_teammate = {  "name": new_teammember.name,
                            "utc_offset": new_teammember.utc_offset,
                            "abbreviation": new_teammember.abbrevation,
                            "timezone": new_teammember.timezone.replace("_"," "),
                            "email": new_teammember.email
                        }
        with open(local_data, mode="r+") as file:
            file.seek(0,2)
            position = file.tell() -1
            file.seek(position)
            file.write( ",\n{}]".format(json.dumps(new_teammate), indent=4, separators=(',', ': ')))
        return(jsonify({"success": f"{new_teammate}"}))
    elif request.method == "GET":
        return_payload = {  "name": new_teammember.name,
                            "utc_offset": new_teammember.utc_offset,
                            "abbreviation": new_teammember.abbrevation,
                            "timezone": new_teammember.timezone.replace("_"," "),
                            "email": new_teammember.email
                        }
                        
        return(jsonify({"success": return_payload}))
    elif request.method == "DELETE":
        data = load_local_db()
        for dict in data:
            if team_member in dict['name']:
                data.remove(dict)
        # l.remove(next(d for d in l if d['name'] == value))
    else:
        return(abort(404))

@app.route("/get_local_time/<string:team_member>", methods=['GET'])
def get_local_time(team_member):
    data = load_local_db()
    # print(data)
    team_member = team_member.capitalize()

    for dict in data:
        # print("")
        # print(dict)
        if team_member in dict['name']:
            timezone = str(dict['timezone']).replace(" ","_")
            api_url = tzdb_url + f"/v2.1/get-time-zone?key={tzdb_api_key}&format=json&by=zone&zone={timezone}"
            tzdb_response = requests.get(api_url).json()
            local_time = tzdb_response['formatted']
            return(jsonify({f"Local time for {team_member}: ": local_time}))
        elif team_member not in dict['name']:
            continue
        else:
            return(abort(404))
    
    
    # if teammate_info:
    #     print(teammate_info)
    #     print(teammate_info['timezone'])
    #     api_url = tzdb_url + f"/v2.1/get-time-zone?key={tzdb_api_key}&format=json&by=zone&zone={teammate_info['timezeone']}"
    #     tzdb_response = requests.get(api_url)
    #     local_time = tzdb_response['data']['formatted']
    #     return(jsonify({f"Local time for {team_member}: ": local_time}))
        
    # else:
    #     return(abort(404))


@app.route("/team/<string:team_member>")
def get_teammate_info(team_member):
    data = load_local_db()
    team_member = team_member.capitalize()
    teammate_info = [dict for dict in data if team_member in dict['name']]
    if teammate_info:
        return(jsonify({f"info for {team_member}: ": teammate_info[0]}))
    else:
        return(abort(404))


if __name__ == "__main__":
    app.run(debug=True, port=8080)
    # city = "Shanghai"
    # country = "Asia"
    # tz = get_tz(city, country)
    # print(tz)
