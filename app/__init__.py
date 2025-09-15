from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="update-jira-status.vercel.app")

from app import routes