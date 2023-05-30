from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Planet, Scientist, Mission

fake = Faker()

def make_scientists():
    
    nerds = []
    for i in range(20):
        s = Scientist(
            name = fake.name(),
            field_of_study = fake.job(),
            avatar = fake.url(),
            updated_at = None
        )
        nerds.append(s)
    db.session.add_all(nerds)
    db.session.commit()

def make_planets():
    planets = []
    for i in range(10):
        p = Planet(
            name = fake.name(),
            distance_from_earth = fake.text(max_nb_chars=20),
            nearest_star = fake.text(max_nb_chars=20),
            image = fake.url(),
        )
        planets.append(p)
    db.session.add_all(planets)
    db.session.commit()

def make_mission():
    missions = []
    for i in range(30):
        m = Mission(
            name = fake.text(max_nb_chars=20),
            scientist_id = randint(1, 20),
            planet_id = randint(1, 10),
        )
        missions.append(m)
    db.session.add_all(missions)
    db.session.commit()




if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        Planet.query.delete()
        Scientist.query.delete()
        Mission.query.delete()

        make_mission()
        make_planets()
        make_scientists()


        print("Done seeding!")
