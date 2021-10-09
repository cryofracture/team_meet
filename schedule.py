import json
from flask import Flask, jsonify, abort
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

team_file = os.environ['TEAM_FILE']

@app.route("/meet/<string:team_member>")
def get_meeting_time(team_member):
    data = json.load(open(f"{team_file}", "r"))