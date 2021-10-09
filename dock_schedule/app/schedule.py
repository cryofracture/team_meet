import os
import json
from flask import Flask, jsonify, abort
from dotenv import load_dotenv
from pathlib import Path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials

load_dotenv()


app = Flask(__name__)

# team_file = os.environ['TEAM_FILE']
# team_file = json.load(open(Path("dock_mongo/data/support-eng.json")))

# class TeamMember:
#     def __init__(self, team_member):
#         team = json.load(open(f"{team_file}"), "r")
#         self.name = ""

@app.route("/meet/<string:team_member>")
def get_meeting_time(team_member):
    data = json.load(open("dock_mongo/data/support-eng.json", "r"))
    teammates = [teammate for teammate in data]
    if team_member in teammates:
        return jsonify({f"info for {team_member}": teammate})
        

if __name__ == "__main__":
    app.run(debug=True)
