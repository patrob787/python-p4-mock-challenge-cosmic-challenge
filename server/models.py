from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
  "ix": "ix_%(column_0_label)s",
  "uq": "uq_%(table_name)s_%(column_0_name)s",
  "ck": "ck_%(table_name)s_%(constraint_name)s",
  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
  "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)

class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.String)
    nearest_star = db.Column(db.String)
    image = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    missions = db.relationship('Mission', backref='planet')

    serialize_rules = ("-missions.planet",)
    serialize_only = ("id", "name", "distance_from_earth", "nearest_star", "image")

    def __repr__(self):
        return f'<Planet {self.id}: {self.name}>'

class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    field_of_study = db.Column(db.String, nullable=False)
    avatar = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    missions = db.relationship('Mission', backref='scientist')

    serialize_rules = ("-missions.scientist",)
    # serialize_only = ("id", "name", "field_of_study", "avatar")

    @validates('name')
    def validate_name(self, key, name):
        if name == None or len(name) < 1:
            raise ValueError("Name must be entered")
        return name
    
    @validates('field_of_study')
    def validate_field_of_study(self, key, field):
        if field == None or len(field) < 1:
            raise ValueError("Scientist must have a field of study")
        return field

    def __repr__(self):
        return f'<Scientist {self.id}: {self.name}>'
    


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    serialize_rules = ("-planet.missions", "-scientist.missions",)
    serialize_only = ("name", "scientist_id", "planet_id")

    @validates('name')
    def validate_name(self, key, name):
        if name == None or len(name) < 1:
            raise ValueError("Name must be entered")
        return name
    
    @validates('scientist_id')
    def validate_scientist(self, key, scientist):
        if scientist == None:
            raise ValueError("Mission must have scientist")
        return scientist
    
    @validates('planet_id')
    def validate_planet(self, key, planet):
        if planet == None:
            raise ValueError("Mission must have planet")
        return planet


# add any models you may need. 