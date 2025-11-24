from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Member, Event, Participation, Due
import os

app = Flask(__name__, instance_relative_config=True)
# Dossier "instance" (Flask le crée si besoin)
os.makedirs(app.instance_path, exist_ok=True)

# Base SQLite dans instance/association.db
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    app.instance_path, "association.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# On relie db à l'application Flask

app.secret_key = "dev-secret-key"

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------- Dashboard ----------
@app.route("/")
def dashboard():
    # ---- 1) Nombre total de membres ----
    members_count = Member.query.count()

    # ---- 2) Pourcentage de cotisations payées ----
    total_dues = Due.query.count()
    dues_paid = Due.query.filter_by(paid=True).count()
    dues_rate = round((dues_paid / total_dues) * 100, 2) if total_dues > 0 else 0

    # ---- 3) Événements à venir ----
    today = date.today()
    events_count = Event.query.filter(Event.event_date > today).count()

    # ---- 4) Derniers membres inscrits ----
    last_members = Member.query.order_by(Member.joined_on.desc()).limit(5).all()

    return render_template(
        "dashboard.html",
        members=members_count,
        dues=dues_rate,
        events=events_count,
        last_members=last_members
    )





# ---------- Members ----------
@app.route("/members")
def members_list():
    q = request.args.get("q", "").strip()
    query = Member.query
    if q:
        like = f"%{q}%"
        query = query.filter(
            (Member.first_name.ilike(like)) |
            (Member.last_name.ilike(like)) |
            (Member.email.ilike(like))
        )
    members = query.order_by(Member.last_name.asc()).all()
    return render_template("members_list.html", members=members, q=q)


@app.route("/members/new", methods=["GET", "POST"])
def members_new():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        email = request.form.get("email", "").strip()

        if not (first_name and last_name and email):
            flash("Tous les champs sont requis.", "danger")
            return redirect(url_for("members_new"))

        status = request.form.get("status")
        m = Member(first_name=first_name, last_name=last_name, email=email, status=status)

        db.session.add(m)

        try:
            db.session.commit()
            flash("Membre créé.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur: {e}", "danger")

        return redirect(url_for("members_list"))

    return render_template("members_form.html", member=None)


@app.route("/members/<int:member_id>/edit", methods=["GET", "POST"])
def members_edit(member_id):
    member = Member.query.get_or_404(member_id)

    if request.method == "POST":
        member.first_name = request.form.get("first_name", "").strip()
        member.last_name = request.form.get("last_name", "").strip()
        member.email = request.form.get("email", "").strip()
        member.status = request.form.get("status")
        
        try:
            db.session.commit()
            flash("Membre mis à jour.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur: {e}", "danger")

        return redirect(url_for("members_list"))

    return render_template("members_form.html", member=member)


@app.route("/members/<int:member_id>/delete", methods=["POST"])
def member_delete(member_id):
    member = Member.query.get_or_404(member_id)
    db.session.delete(member)
    db.session.commit()
    flash("Membre supprimé.", "success")
    return redirect(url_for("members_list"))


# ---------- Events ----------
@app.route("/events")
def events_list():
    events = Event.query.order_by(Event.event_date.desc()).all()
    return render_template("events_list.html", events=events)


@app.route("/events/new", methods=["GET", "POST"])
def events_new():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        event_date = request.form.get("event_date", "").strip()
        location = request.form.get("location", "").strip()
        description = request.form.get("description", "").strip()

        if not (title and event_date):
            flash("Titre et date requis.", "danger")
            return redirect(url_for("events_new"))

        try:
            dt = datetime.strptime(event_date, "%Y-%m-%d").date()
        except ValueError:
            flash("Format de date invalide.", "danger")
            return redirect(url_for("events_new"))

        e = Event(title=title, event_date=dt, location=location, description=description)
        db.session.add(e)
        db.session.commit()

        flash("Événement créé.", "success")
        return redirect(url_for("events_list"))

    return render_template("events_form.html", event=None)


@app.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
def events_edit(event_id):
    event = Event.query.get_or_404(event_id)

    if request.method == "POST":
        event.title = request.form.get("title", "").strip()
        event_date = request.form.get("event_date", "").strip()
        event.location = request.form.get("location", "").strip()
        event.description = request.form.get("description", "").strip()

        try:
            event.event_date = datetime.strptime(event_date, "%Y-%m-%d").date()
        except ValueError:
            flash("Format de date invalide.", "danger")
            return redirect(url_for("events_edit", event_id=event.id))

        db.session.commit()
        flash("Événement mis à jour.", "success")
        return redirect(url_for("events_list"))

    return render_template("events_form.html", event=event)


@app.route("/events/<int:event_id>/delete", methods=["POST"])
def events_delete(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Événement supprimé.", "success")
    return redirect(url_for("events_list"))


# ---------- Participations ----------

# ---------- Participations ----------

@app.route("/participations")
def participations_list():
    participations = Participation.query.order_by(Participation.id.desc()).all()
    return render_template("participations_list.html", participations=participations)


@app.route("/participations/new", methods=["GET", "POST"])
def participations_new():
    members = Member.query.order_by(Member.last_name.asc()).all()
    events = Event.query.order_by(Event.event_date.desc()).all()

    if request.method == "POST":
        member_id = int(request.form.get("member_id"))
        event_id = int(request.form.get("event_id"))
        status = request.form.get("status", "inscrit")

        # 🔍 Vérifier si la participation existe déjà :
        existing = Participation.query.filter_by(member_id=member_id, event_id=event_id).first()
        if existing:
            flash("⚠️ Ce membre est déjà inscrit à cet événement.", "danger")
            return redirect(url_for("participations_new"))

        p = Participation(member_id=member_id, event_id=event_id, status=status)
        db.session.add(p)

        try:
            db.session.commit()
            flash("Participation ajoutée avec succès.", "success")
        except:
            db.session.rollback()
            flash("Erreur interne lors de l’enregistrement.", "danger")

        return redirect(url_for("participations_list"))

    return render_template("participations_form.html", members=members, events=events)


@app.route("/participations/<int:pid>/edit", methods=["GET", "POST"])
def participations_edit(pid):
    p = Participation.query.get_or_404(pid)
    members = Member.query.order_by(Member.last_name.asc()).all()
    events = Event.query.order_by(Event.event_date.desc()).all()

    if request.method == "POST":
        member_id = int(request.form.get("member_id"))
        event_id = int(request.form.get("event_id"))
        status = request.form.get("status", "inscrit")

        # 🔍 Vérifier si cette combinaison existe pour un autre enregistrement
        existing = Participation.query.filter(
            Participation.member_id == member_id,
            Participation.event_id == event_id,
            Participation.id != pid
        ).first()

        if existing:
            flash("⚠️ Ce membre est déjà inscrit à cet événement.", "danger")
            return redirect(url_for("participations_edit", pid=pid))

        p.member_id = member_id
        p.event_id = event_id
        p.status = status

        try:
            db.session.commit()
            flash("Participation modifiée avec succès.", "success")
        except:
            db.session.rollback()
            flash("Erreur interne lors de la modification.", "danger")

        return redirect(url_for("participations_list"))

    return render_template("participations_form.html", participation=p, members=members, events=events)


@app.route("/participations/<int:pid>/delete", methods=["POST"])
def participations_delete(pid):
    p = Participation.query.get_or_404(pid)
    db.session.delete(p)

    try:
        db.session.commit()
        flash("Participation supprimée avec succès.", "success")
    except:
        db.session.rollback()
        flash("Erreur lors de la suppression.", "danger")

    return redirect(url_for("participations_list"))



# ---------- Dues (Cotisations) ----------
@app.route("/dues")
def dues_list():
    dues = Due.query.order_by(Due.year.desc()).all()
    return render_template("dues_list.html", dues=dues)


@app.route("/dues/new", methods=["GET", "POST"])
def dues_new():
    members = Member.query.order_by(Member.last_name.asc()).all()

    if request.method == "POST":
        member_id = int(request.form.get("member_id"))
        year = int(request.form.get("year"))
        amount = float(request.form.get("amount"))
        paid = True if request.form.get("paid") == "on" else False

        d = Due(member_id=member_id, year=year, amount=amount, paid=paid)
        db.session.add(d)

        try:
            db.session.commit()
            flash("Cotisation ajoutée.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur: {e}", "danger")

        return redirect(url_for("dues_list"))

    return render_template("dues_form.html", members=members)


@app.route("/dues/<int:due_id>/edit", methods=["GET", "POST"])
def dues_edit(due_id):
    due = Due.query.get_or_404(due_id)
    members = Member.query.order_by(Member.last_name.asc()).all()

    if request.method == "POST":
        due.member_id = int(request.form.get("member_id"))
        due.year = int(request.form.get("year"))
        due.amount = float(request.form.get("amount"))
        due.paid = True if request.form.get("paid") == "on" else False

        try:
            db.session.commit()
            flash("Cotisation mise à jour.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Erreur: {e}", "danger")

        return redirect(url_for("dues_list"))

    return render_template("dues_form.html", members=members, due=due)


@app.route("/dues/<int:due_id>/delete", methods=["POST"])
def dues_delete(due_id):
    due = Due.query.get_or_404(due_id)
    db.session.delete(due)
    db.session.commit()
    flash("Cotisation supprimée.", "success")
    return redirect(url_for("dues_list"))

# Création des tables dans la base (si elles n'existent pas)
with app.app_context():
    db.create_all()

# ---------- Run ----------
if __name__ == "__main__":
    app.run(debug=True)
