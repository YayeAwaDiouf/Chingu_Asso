from datetime import date
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Member(db.Model):
    __tablename__ = "members"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    joined_on = db.Column(db.Date, default=date.today, nullable=False)
    status = db.Column(db.String(20), default="Actif")
    participations = db.relationship("Participation", back_populates="member", cascade="all, delete-orphan")
    dues = db.relationship("Due", back_populates="member", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Member {self.first_name} {self.last_name}>"

class Event(db.Model):
    __tablename__ = "events"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    location = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)

    participations = db.relationship("Participation", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Event {self.title} {self.event_date}>"

class Participation(db.Model):
    __tablename__ = "participations"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.id"), nullable=False)
    status = db.Column(db.String(50), default="inscrit")  # inscrit / présent / absent

    member = db.relationship("Member", back_populates="participations")
    event = db.relationship("Event", back_populates="participations")

    __table_args__ = (
        db.UniqueConstraint("member_id", "event_id", name="uq_member_event"),
    )

    def __repr__(self):
        return f"<Participation member={self.member_id} event={self.event_id}>"

class Due(db.Model):
    __tablename__ = "dues"
    id = db.Column(db.Integer, primary_key=True)
    member_id = db.Column(db.Integer, db.ForeignKey("members.id"), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False, default=20.0)
    paid = db.Column(db.Boolean, nullable=False, default=False)

    member = db.relationship("Member", back_populates="dues")

    __table_args__ = (
        db.UniqueConstraint("member_id", "year", name="uq_member_year"),
    )

    def __repr__(self):
        return f"<Due member={self.member_id} year={self.year} paid={self.paid}>"
