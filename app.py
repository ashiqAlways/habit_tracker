from datetime import date
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-password-secret-key'

db = SQLAlchemy(app)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    color = db.Column(db.String(9), default="#3b82f6")
    goal_type = db.Column(db.String(20), default='daily')
    target_per_day = db.Column(db.Integer, default=1)
    created_at = db.Column(db.Date, default=date.today)
    


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/habits')
def habits():


    habits = Habit.query.order_by(Habit.created_at.desc()).all()
    return render_template('habits.html', habits=habits)


@app.route('/habits/create', methods=["POST"])
def create_habit():
    name = request.form.get("name", "").strip()
    color = request.form.get('color', '#3b82f6').strip()

    if not name:
        flash('Name is required', 'error')
        return redirect(url_for('habits'))

    try:
        habit = Habit(name=name, color=color)
        db.session.add(habit)
        db.session.commit()
        flash('Habit Created', 'success')

    except Exception:
        db.session.rollback()
        flash('Habit name must be unquique', 'error')

    return redirect(url_for('habits'))



@app.route('/habits/<int:habit_id>/delete', methods=["POST"])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)

    try:
        db.session.delete(habit)
        db.session.commit()
        flash("Habit deleted successfully!", "success")

    except Exception:
        db.session.rollback()
        flash("Error deleting habit. Try again.", "error")

    return redirect(url_for('habits'))




if __name__ == '__main__':
    app.run(debug=True, port=3535)
