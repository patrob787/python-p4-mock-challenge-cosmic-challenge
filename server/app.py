#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from flask_cors import CORS

from models import db, Planet, Scientist, Mission

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
CORS(app)

db.init_app(app)
api = Api(app)

@app.route('/')
def home():
    return 'This is our home!'

class Scientists(Resource):
    def get(self):
        scientists = [s.to_dict(only=("id", "name", "field_of_study", "avatar")) for s in Scientist.query.all()]

        resp = make_response(scientists, 200)
        return resp
    
    def post(self):
        new_scientist = Scientist(
            name = request.form['name'],
            field_of_study = request.form['field_of_study'],
            avatar = request.form['avatar'],
        )

        if new_scientist:
            db.session.add(new_scientist)
            db.session.commit()

            sci_dict = new_scientist.to_dict()

            resp = make_response(sci_dict, 201)
            return resp
        else:
            resp = make_response({"error": "400: Validation error"}, 400)
            return resp
    
api.add_resource(Scientists, '/scientists')

class ScientistById(Resource):
    def get(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()

        if scientist:
            resp = make_response(scientist.to_dict(only=("id", "name", "field_of_study", "avatar")), 200)
        else:
            resp = make_response({"error": "404: Scientist not found"}, 404)
        
        return resp
    
    def patch(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()

        for attr in request.form:
            setattr(scientist, attr, request.form[attr])

        if scientist:
            db.session.add(scientist)
            db.session.commit()

            resp = make_response(scientist.to_dict(), 202)

        else:
            resp = make_response({"error": "400: Validation error"}, 400)

        return resp
    
    def delete(self, id):
        scientist = Scientist.query.filter(Scientist.id == id).first()

        if scientist:
            db.session.delete(scientist)
            db.session.commit()

            resp = make_response({"message": "delete successful"})
            
        else:
            resp = make_response({"error": "404: Scientist not found"}, 404)
            
        return resp
    
api.add_resource(ScientistById, "/scientists/<int:id>")

class Planets(Resource):
    def get(self):
        planets = [p.to_dict() for p in Planet.query.all()]

        resp = make_response(planets, 200)
        return resp
    
api.add_resource(Planets, "/planets")

class Missions(Resource):
    def post(self):
        new_mission = Mission(
            name = request.form['name'],
            scientist_id = request.form['scientist_id'],
            planet_id = request.form['planet_id'],
        )

        if new_mission:
            db.session.add(new_mission)
            db.session.commit()

            planet_dict = Planet.query.filter(Planet.id == request.form['planet_id']).first().to_dict()
            resp = make_response(planet_dict, 201)
        
        else:
            resp = make_response({"error": "400: Validation error"}, 400)

        return resp
    
api.add_resource(Missions, "/missions")

if __name__ == '__main__':
    app.run(port=5555, debug=True)
