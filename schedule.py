import json
from flask import Flask, jsonify, abort
from dotenv import load_dotenv
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
load_dotenv()


app = Flask(__name__)

team_file = os.environ['TEAM_FILE']

class TeamMember:
    def __init__(self, team_member):
        team = json.load(open(f"{team_file}"), "r")
        self.name = 

@app.route("/meet/<string:team_member>")
def get_meeting_time(team_member):
    data = json.load(open(f"{team_file}", "r"))
    team_members = [teammate for teammate in data]
    if team_member in team_members:
        return jsonify(team_member)
        

if __name__ == "__main__":
    app.run(debug=True)
