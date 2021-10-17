#!/usr/bin/env/python

##################################################################################################################
#                                                                                                                #
#                                                   Imports                                                      #
#                                                                                                                #
##################################################################################################################

import os
import json
from flask import Flask, jsonify, abort, request, Response # type: ignore
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
import requests
import re
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials


# Load environment variables - will replace will a cloud API call to secrets manager software.
# Current frontrunner: self-hosted vault.
load_dotenv(find_dotenv())
tzdb_api_key = os.environ['TZDB_API_KEY']
tzdb_url = os.environ['TZDB_URL']
# local_data = os.environ['TEAM_FILE']
local_data = "/src/mock_data/support-eng.json"


app = Flask(__name__)


##################################################################################################################
#                                                                                                                #
#                                           Classes and functions                                                #
#                                                                                                                #
##################################################################################################################


class CreateTeamMember:
    # CreateTeamMember assembles data into an object that can be inserted to the db.
    def __init__(self, team_member, city, country, email):
        # TODO: move TZDB API request to function
        api_url = tzdb_url + f"/v2.1/get-time-zone?key={tzdb_api_key}&format=json&by=zone&zone={country}/{city}"
        tz = requests.get(api_url).json()

        # Ensure name is capitalized for prettier text.
        self.name = str(team_member.capitalize())

        # call utc_offset function which divides utc_offset by minutes, and then hours to determine UTC offset.
        # example output of this would be: UTC+8, UTC-4 UTC+0
        self.utc_offset = "UTC" + str(get_utc_offset(tz['gmtOffset']))

        # e.g. CET, AST, PDT
        self.abbrevation = tz['abbreviation']

        # string representation of city in that timezone
        # e.g. America/Los_Angeles, Europe/Dublin, Europe/Paris, Asia/Shanghai
        self.timezone = tz['zoneName']

        # email address verified:
        
        self.email = verify_email(email)

    # Give the newly created object back after construction.
    def returnNewMember(self):
        return CreateTeamMember()

def verify_email(email_address):
    # match all acceptable characters before and after "@", includes a ".", and has a domain of at least 2 characters
    email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

    # Full match of regex against provided email address. If it passes, return the email, if it fails the regex, return a bad request.
    if re.fullmatch(email_regex,email_address):
        return email_address
    elif not re.fullmatch(email_regex,email_address):
        return(Response("Error, invalid email address provided.", status=400))

# Function to calculate GMT Offset (in hours) from the TZDB API response, which is in milliseconds.
# For readability, though hours and minutes equal the same, I differentiated these variables so there's no "magic numbers" floating around.
def get_utc_offset(gmtOffset):
    hour = 60
    minute = 60
    # convert calculated result from a float to an int, stripping the decimal for a more standard "UTC+x" display.
    utc_offset = int(gmtOffset / hour / minute)
    return utc_offset

# For local dev while mongo container is not operational. 
# Will implement a "build env" check to determine if we are local or in a docker container and where to load data from eventually.
def load_local_db():
    data = json.load(open(local_data, "r"))
    return data

##################################################################################################################
#                                                                                                                #
#                                                   API ROUTES                                                   #
#                                                                                                                #
##################################################################################################################

# Create a new team member. For proper API functionality, all fields are currently required.
@app.route('/api/create-teammember/<string:team_member>', methods=['GET','PUT','DELETE'])
def create_teammember(team_member):
    # Pull arguments from GET request. URL example would be:
    # curl -X GET|PUT /api/create-teammember/Newguy?city=New York&country=America&email=Newguy@acme.co
    # submitting a GET will simulate creating a teammember, ensuring proper field population.
    # submitting a PUT will submit the user to the db.
    city = request.args.get('city')
    country = request.args.get('country')
    email = request.args.get('email')
    args = [city,country,email]
    for arg in args:
        if arg is None:
            return(abort(400))
    new_teammember = CreateTeamMember(team_member, city.replace(" ","_"), country, email)
    
    # TODO: revamp PUT creation. Inlcude build env check as discussed above, if local dev, overrwrite a file, if mongodb is up, just insert new object to table.
    if request.method == "PUT":
        new_teammate = {  "name": new_teammember.name,
                            "utc_offset": new_teammember.utc_offset,
                            "abbreviation": new_teammember.abbrevation,
                            "timezone": new_teammember.timezone.replace("_"," "),
                            "email": new_teammember.email
                        }
        # Opens the local json data in a reading+ format, allowing us to read all the data of the file and write new data to the file.
        with open(local_data, mode="r+") as file:
            # Use open file to skip the end of the file, and move cursor back 1 character, behind the closing ']'
            file.seek(0,2)
            position = file.tell() -1
            file.seek(position)
            
            # Write to the file a comma after the last json object, newline, json object of the json dumps of new_teammate,and new closing bracket (old bracket overwritten, needs to be re-added to keep proper json)
            file.write( ",\n{}]".format(json.dumps(new_teammate), indent=4, separators=(',', ': ')))
        return(jsonify({"success": f"{new_teammate}"}))
    
    # GET requests are handled as basically a simulation of creating a new teammember.
    elif request.method == "GET":
        return_payload = {  "name": new_teammember.name,
                            "utc_offset": new_teammember.utc_offset,
                            "abbreviation": new_teammember.abbrevation,
                            "timezone": new_teammember.timezone.replace("_"," "),
                            "email": new_teammember.email
                        }
                        
        return(jsonify({"success": return_payload}))
    
    # TODO: finish delete request functionality. Expected flow:
    # load data (local or from mongo)
    # search through all objects/rows for one that contains the teammember's name in the object's 'Name' value.
    # remove that object/row from the db.
    elif request.method == "DELETE":
        data = load_local_db()
        for dict in data:
            if team_member in dict['name']:
                data.remove(dict)
    
    # any other request method is rejected as a 400 - Bad Request
    else:
        return(abort(400))

# Using the timezone information from the database, reach back to the TZDB API to get current local time for provided teammember's location.
@app.route("/api/get_local_time/<string:team_member>", methods=['GET'])
def get_local_time(team_member):
    data = load_local_db()
    team_member = team_member.capitalize()

    for dict in data:
        if team_member in dict['name']:
            # Database stores timezone with spaces like: America/Los Angeles, API needs " " converted to "_"
            timezone = str(dict['timezone']).replace(" ","_")
            # TODO: move TZDB API requests to a better built function that customizes the url based on the endpoint accessed, providing a more scalable solution for API URL implementation.
            api_url = tzdb_url + f"/v2.1/get-time-zone?key={tzdb_api_key}&format=json&by=zone&zone={timezone}"
            tzdb_response = requests.get(api_url).json()
            local_time = tzdb_response['formatted']
            return(jsonify({f"Local time for {team_member}: ": local_time}))
        else:
            return(abort(404))

# function to print out all information on the requested teammember, including:
# Name, email, UTC Offset, Timezone, Timezone Abbreviation.
@app.route("/api/team/<string:team_member>")
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