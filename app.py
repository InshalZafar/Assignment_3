from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Destination, Review, TravelPlan, travel_plan_destination
from forms import RegistrationForm, LoginForm, DestinationForm, ReviewForm, TravelPlanForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key')
# app.config['SECRET_KEY'] = 'tourism-explorer-secret-key-12345'

database_url = os.environ.get('DATABASE_URL')
if not database_url:
    db_host = os.environ.get('DB_HOST')
    if db_host:
        db_user = os.environ.get('DB_USER', 'root')
        db_password = os.environ.get('DB_PASSWORD', 'rootpassword')
        db_name = os.environ.get('DB_NAME', 'flask_app_db')
        database_url = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
    else:
        database_url = 'sqlite:///tourism.db'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    destinations = Destination.query.all()
    return render_template('index.html', destinations=destinations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/destinations')
@login_required
def destinations():
    destinations = Destination.query.all()
    return render_template('destinations.html', destinations=destinations)

@app.route('/destination/<int:id>', methods=['GET', 'POST'])
@login_required
def destination_detail(id):
    destination = Destination.query.get_or_404(id)
    form = ReviewForm()
    if form.validate_on_submit():
        review = Review(content=form.content.data, rating=form.rating.data, user_id=current_user.id, destination_id=id)
        db.session.add(review)
        db.session.commit()
        flash('Review added!')
        return redirect(url_for('destination_detail', id=id))
    return render_template('destination_detail.html', destination=destination, form=form)

@app.route('/add_destination', methods=['GET', 'POST'])
@login_required
def add_destination():
    form = DestinationForm()
    if form.validate_on_submit():
        destination = Destination(name=form.name.data, description=form.description.data, location=form.location.data, image_url=form.image_url.data)
        db.session.add(destination)
        db.session.commit()
        flash('Destination added!')
        return redirect(url_for('destinations'))
    return render_template('destination_form.html', form=form)

@app.route('/edit_destination/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_destination(id):
    destination = Destination.query.get_or_404(id)
    form = DestinationForm(obj=destination)
    if form.validate_on_submit():
        destination.name = form.name.data
        destination.description = form.description.data
        destination.location = form.location.data
        destination.image_url = form.image_url.data
        db.session.commit()
        flash('Destination updated!')
        return redirect(url_for('destinations'))
    return render_template('destination_form.html', form=form, destination=destination)

@app.route('/delete_destination/<int:id>', methods=['POST'])
@login_required
def delete_destination(id):
    destination = Destination.query.get_or_404(id)
    db.session.delete(destination)
    db.session.commit()
    flash('Destination deleted!')
    return redirect(url_for('destinations'))

@app.route('/travel_plans')
@login_required
def travel_plans():
    plans = TravelPlan.query.filter_by(user_id=current_user.id).all()
    return render_template('travel_plans.html', plans=plans)

@app.route('/create_plan', methods=['GET', 'POST'])
@login_required
def create_plan():
    form = TravelPlanForm()
    if form.validate_on_submit():
        plan = TravelPlan(name=form.name.data, user_id=current_user.id)
        db.session.add(plan)
        db.session.commit()
        flash('Plan created!')
        return redirect(url_for('travel_plans'))
    return render_template('create_plan.html', form=form)

@app.route('/add_destination_to_plan/<int:plan_id>', methods=['GET', 'POST'])
@login_required
def add_destination_to_plan(plan_id):
    plan = TravelPlan.query.get_or_404(plan_id)
    if plan.user_id != current_user.id:
        flash('Unauthorized')
        return redirect(url_for('travel_plans'))
    destinations = Destination.query.all()
    if request.method == 'POST':
        dest_id = request.form.get('destination_id')
        dest = Destination.query.get(dest_id)
        if dest and dest not in plan.destinations:
            plan.destinations.append(dest)
            db.session.commit()
            flash('Destination added to plan!')
        return redirect(url_for('travel_plans'))
    return render_template('add_destination_to_plan.html', plan=plan, destinations=destinations)

@app.route('/remove_from_plan/<int:plan_id>/<int:dest_id>')
@login_required
def remove_from_plan(plan_id, dest_id):
    plan = TravelPlan.query.get_or_404(plan_id)
    if plan.user_id != current_user.id:
        flash('Unauthorized')
        return redirect(url_for('travel_plans'))
    dest = Destination.query.get(dest_id)
    if dest in plan.destinations:
        plan.destinations.remove(dest)
        db.session.commit()
        flash('Destination removed from plan!')
    return redirect(url_for('travel_plans'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()