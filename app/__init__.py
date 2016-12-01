from flask import Flask
from sqlalchemy import create_engine

#create mysql user 'app' and grant read only on project db
db_engine = create_engine('mysql+pymysql://app:password@localhost:3306/project')

app = Flask(__name__)
from app import views
