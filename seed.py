from app import app
from models import db, Member, Event, Due, Participation
from datetime import date, timedelta
import random, faker

fake = faker.Faker()

with app.app_context():
    print("Réinitialisation de la base...")
    db.drop_all()
    db.create_all()

    # ===== Membres =====
    print("Création des membres...")
    members = []
    for _ in range(25):
        m = Member(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            joined_on=fake.date_between(start_date="-2y", end_date="today")
        )
        members.append(m)
        db.session.add(m)
    db.session.commit()

    # ===== Cotisations =====
    print("Ajout des cotisations...")
    for m in members:
        paid = random.choice([True, False, False])  # 1/3 payés, 2/3 non payés
        d = Due(
            member_id=m.id,
            year=2025,
            amount=random.choice([5000, 10000, 15000]),
            paid=paid
        )
        db.session.add(d)
    db.session.commit()

    # ===== Création des événements =====
    print("Création des événements...")
    events = []
    for _ in range(10):
        e = Event(
            title=fake.catch_phrase(),
            event_date=date.today() + timedelta(days=random.randint(3, 120)),
            location=fake.city(),
            description=fake.text(max_nb_chars=200)
        )
        events.append(e)
        db.session.add(e)
    db.session.commit()

    # ===== Participations =====
    print("Ajout des participations...")
    for e in events:
        participants = random.sample(members, random.randint(5, 20))
        for p in participants:
            participation = Participation(
                member_id=p.id,
                event_id=e.id,
                status=random.choice(["inscrit", "présent", "absent"])
            )
            db.session.add(participation)
    db.session.commit()

    print("🎉 Base remplie avec succès avec 25 membres, 10 événements et des cotisations réalistes !")
