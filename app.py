import os
from datetime import datetime
from flask import (Flask, render_template, redirect, url_for, flash, request,
                   jsonify, abort)
from flask_login import (LoginManager, login_user, login_required, logout_user,
                         current_user)
from sqlalchemy import or_, func

from models import (db, User, Destination, DestinationImage, Review, Reply,
                    TravelPlan, Wishlist, travel_plan_destination, CATEGORIES)
from forms import (RegistrationForm, LoginForm, DestinationForm, ReviewForm,
                   ReplyForm, TravelPlanForm, ProfileForm, SearchForm)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tourism-explorer-secret-key-12345')
    app.config['WTF_CSRF_ENABLED'] = False  # disabled for selenium tests

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

    @app.context_processor
    def inject_globals():
        wishlist_ids = set()
        if current_user.is_authenticated:
            wishlist_ids = {w.destination_id for w in current_user.wishlist_items}
        return {
            'CATEGORIES': CATEGORIES,
            'wishlist_ids': wishlist_ids,
            'current_year': datetime.utcnow().year,
        }

    # ---------------- Public ----------------
    @app.route('/')
    def index():
        destinations = Destination.query.all()
        trending = sorted(destinations, key=lambda d: d.review_count, reverse=True)[:6]
        top_rated = sorted(destinations, key=lambda d: d.avg_rating, reverse=True)[:6]
        stats = {
            'destinations': len(destinations),
            'reviews': Review.query.count(),
            'travelers': User.query.count(),
            'plans': TravelPlan.query.count(),
        }
        return render_template('index.html', destinations=destinations,
                               trending=trending, top_rated=top_rated, stats=stats)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            existing = User.query.filter(
                or_(User.email == form.email.data, User.username == form.username.data)
            ).first()
            if existing:
                flash('That email or username is already in use.', 'error')
            else:
                user = User(username=form.username.data, email=form.email.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('Welcome aboard! Please sign in.', 'success')
                return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash(f'Welcome back, {user.username}.', 'success')
                return redirect(url_for('index'))
            flash('Invalid email or password.', 'error')
        return render_template('login.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('You have been signed out.', 'success')
        return redirect(url_for('index'))

    # ---------------- Destinations ----------------
    @app.route('/destinations')
    def destinations():
        destinations = Destination.query.order_by(Destination.created_at.desc()).all()
        return render_template('destinations.html', destinations=destinations,
                               heading='All Destinations')

    @app.route('/category/<name>')
    def category(name):
        if name not in CATEGORIES:
            abort(404)
        destinations = Destination.query.filter_by(category=name).all()
        return render_template('category.html', destinations=destinations,
                               category_name=name)

    @app.route('/search')
    def search():
        form = SearchForm(request.args, meta={'csrf': False})
        q = (request.args.get('q') or '').strip()
        cat = request.args.get('category', '') or ''
        try:
            min_rating = int(request.args.get('min_rating') or 0)
        except ValueError:
            min_rating = 0

        query = Destination.query
        if q:
            like = f'%{q}%'
            query = query.filter(or_(
                Destination.name.ilike(like),
                Destination.location.ilike(like),
                Destination.country.ilike(like),
                Destination.description.ilike(like),
            ))
        if cat:
            query = query.filter_by(category=cat)
        results = query.all()
        if min_rating > 0:
            results = [d for d in results if d.avg_rating >= min_rating]
        return render_template('search.html', form=form, results=results,
                               q=q, category=cat, min_rating=min_rating)

    @app.route('/destination/<int:id>', methods=['GET', 'POST'])
    def destination_detail(id):
        destination = Destination.query.get_or_404(id)
        form = ReviewForm()
        reply_form = ReplyForm()
        if form.validate_on_submit():
            if not current_user.is_authenticated:
                flash('Please sign in to leave a review.', 'error')
                return redirect(url_for('login'))
            review = Review(content=form.content.data, rating=int(form.rating.data),
                            user_id=current_user.id, destination_id=id)
            db.session.add(review)
            db.session.commit()
            flash('Review posted.', 'success')
            return redirect(url_for('destination_detail', id=id))
        return render_template('destination_detail.html', destination=destination,
                               form=form, reply_form=reply_form)

    @app.route('/add_destination', methods=['GET', 'POST'])
    @login_required
    def add_destination():
        form = DestinationForm()
        if form.validate_on_submit():
            destination = Destination(
                name=form.name.data,
                description=form.description.data,
                location=form.location.data,
                country=form.country.data or '',
                category=form.category.data,
                image_url=form.image_url.data,
                latitude=form.latitude.data or 0.0,
                longitude=form.longitude.data or 0.0,
            )
            db.session.add(destination)
            db.session.commit()
            flash('Destination added.', 'success')
            return redirect(url_for('destination_detail', id=destination.id))
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
            destination.country = form.country.data or ''
            destination.category = form.category.data
            destination.image_url = form.image_url.data
            destination.latitude = form.latitude.data or 0.0
            destination.longitude = form.longitude.data or 0.0
            db.session.commit()
            flash('Destination updated.', 'success')
            return redirect(url_for('destination_detail', id=id))
        return render_template('destination_form.html', form=form, destination=destination)

    @app.route('/delete_destination/<int:id>', methods=['POST'])
    @login_required
    def delete_destination(id):
        destination = Destination.query.get_or_404(id)
        db.session.delete(destination)
        db.session.commit()
        flash('Destination deleted.', 'success')
        return redirect(url_for('destinations'))

    # ---------------- Reviews / Replies ----------------
    @app.route('/review/<int:id>/reply', methods=['POST'])
    @login_required
    def reply_to_review(id):
        review = Review.query.get_or_404(id)
        form = ReplyForm()
        if form.validate_on_submit():
            reply = Reply(content=form.content.data, user_id=current_user.id, review_id=id)
            db.session.add(reply)
            db.session.commit()
            flash('Reply posted.', 'success')
        return redirect(url_for('destination_detail', id=review.destination_id))

    # ---------------- Wishlist ----------------
    @app.route('/wishlist')
    @login_required
    def wishlist():
        items = Wishlist.query.filter_by(user_id=current_user.id).all()
        destinations = [w.destination for w in items]
        return render_template('wishlist.html', destinations=destinations)

    @app.route('/wishlist/toggle/<int:dest_id>', methods=['POST', 'GET'])
    @login_required
    def wishlist_toggle(dest_id):
        Destination.query.get_or_404(dest_id)
        existing = Wishlist.query.filter_by(user_id=current_user.id, destination_id=dest_id).first()
        if existing:
            db.session.delete(existing)
            db.session.commit()
            flash('Removed from wishlist.', 'success')
            added = False
        else:
            db.session.add(Wishlist(user_id=current_user.id, destination_id=dest_id))
            db.session.commit()
            flash('Saved to wishlist.', 'success')
            added = True
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'added': added})
        return redirect(request.referrer or url_for('destinations'))

    # ---------------- Travel Plans ----------------
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
            plan = TravelPlan(
                name=form.name.data,
                user_id=current_user.id,
                start_date=form.start_date.data,
                end_date=form.end_date.data,
                budget=form.budget.data or 0.0,
                notes=form.notes.data or '',
            )
            db.session.add(plan)
            db.session.commit()
            flash('Plan created.', 'success')
            return redirect(url_for('plan_detail', plan_id=plan.id))
        return render_template('create_plan.html', form=form)

    @app.route('/plan/<int:plan_id>')
    @login_required
    def plan_detail(plan_id):
        plan = TravelPlan.query.get_or_404(plan_id)
        if plan.user_id != current_user.id:
            flash('Unauthorized', 'error')
            return redirect(url_for('travel_plans'))
        return render_template('plan_detail.html', plan=plan)

    @app.route('/edit_plan/<int:plan_id>', methods=['GET', 'POST'])
    @login_required
    def edit_plan(plan_id):
        plan = TravelPlan.query.get_or_404(plan_id)
        if plan.user_id != current_user.id:
            abort(403)
        form = TravelPlanForm(obj=plan)
        if form.validate_on_submit():
            plan.name = form.name.data
            plan.start_date = form.start_date.data
            plan.end_date = form.end_date.data
            plan.budget = form.budget.data or 0.0
            plan.notes = form.notes.data or ''
            db.session.commit()
            flash('Plan updated.', 'success')
            return redirect(url_for('plan_detail', plan_id=plan.id))
        return render_template('create_plan.html', form=form, edit=True, plan=plan)

    @app.route('/delete_plan/<int:plan_id>', methods=['POST'])
    @login_required
    def delete_plan(plan_id):
        plan = TravelPlan.query.get_or_404(plan_id)
        if plan.user_id != current_user.id:
            abort(403)
        db.session.delete(plan)
        db.session.commit()
        flash('Plan deleted.', 'success')
        return redirect(url_for('travel_plans'))

    @app.route('/add_destination_to_plan/<int:plan_id>', methods=['GET', 'POST'])
    @login_required
    def add_destination_to_plan(plan_id):
        plan = TravelPlan.query.get_or_404(plan_id)
        if plan.user_id != current_user.id:
            flash('Unauthorized', 'error')
            return redirect(url_for('travel_plans'))
        destinations = Destination.query.all()
        if request.method == 'POST':
            dest_id = request.form.get('destination_id')
            dest = Destination.query.get(dest_id)
            if dest and dest not in plan.destinations:
                plan.destinations.append(dest)
                db.session.commit()
                flash('Destination added to plan.', 'success')
            return redirect(url_for('plan_detail', plan_id=plan.id))
        return render_template('add_destination_to_plan.html', plan=plan, destinations=destinations)

    @app.route('/remove_from_plan/<int:plan_id>/<int:dest_id>')
    @login_required
    def remove_from_plan(plan_id, dest_id):
        plan = TravelPlan.query.get_or_404(plan_id)
        if plan.user_id != current_user.id:
            flash('Unauthorized', 'error')
            return redirect(url_for('travel_plans'))
        dest = Destination.query.get(dest_id)
        if dest in plan.destinations:
            plan.destinations.remove(dest)
            db.session.commit()
            flash('Destination removed from plan.', 'success')
        return redirect(url_for('plan_detail', plan_id=plan.id))

    # ---------------- Profile ----------------
    @app.route('/profile/<username>', methods=['GET', 'POST'])
    def profile(username):
        user = User.query.filter_by(username=username).first_or_404()
        form = ProfileForm(obj=user) if (current_user.is_authenticated and current_user.id == user.id) else None
        if form and form.validate_on_submit():
            user.bio = form.bio.data or ''
            user.avatar_color = form.avatar_color.data or '#d4af37'
            db.session.commit()
            flash('Profile updated.', 'success')
            return redirect(url_for('profile', username=user.username))
        stats = {
            'reviews': len(user.reviews),
            'plans': len(user.travel_plans),
            'wishlist': len(user.wishlist_items),
        }
        return render_template('profile.html', user=user, stats=stats, form=form)

    # ---------------- Map / Dashboard ----------------
    @app.route('/map')
    def world_map():
        destinations = Destination.query.all()
        pins = [{
            'id': d.id, 'name': d.name, 'location': d.location,
            'country': d.country, 'category': d.category,
            'lat': d.latitude, 'lng': d.longitude,
            'image': d.image_url, 'rating': d.avg_rating,
        } for d in destinations if d.latitude or d.longitude]
        return render_template('map.html', pins=pins, total=len(pins))

    @app.route('/dashboard')
    def dashboard():
        destinations = Destination.query.all()
        top_rated = sorted([d for d in destinations if d.review_count > 0],
                           key=lambda d: (d.avg_rating, d.review_count), reverse=True)[:5]
        most_reviewed = sorted(destinations, key=lambda d: d.review_count, reverse=True)[:5]
        category_counts = {c: 0 for c in CATEGORIES}
        for d in destinations:
            if d.category in category_counts:
                category_counts[d.category] += 1
        top_users = (db.session.query(User, func.count(Review.id).label('rc'))
                     .outerjoin(Review).group_by(User.id)
                     .order_by(func.count(Review.id).desc()).limit(5).all())
        stats = {
            'destinations': len(destinations),
            'reviews': Review.query.count(),
            'travelers': User.query.count(),
            'plans': TravelPlan.query.count(),
            'replies': Reply.query.count(),
            'wishlists': Wishlist.query.count(),
        }
        return render_template('dashboard.html', stats=stats, top_rated=top_rated,
                               most_reviewed=most_reviewed,
                               category_counts=category_counts, top_users=top_users)

    # ---------------- Errors ----------------
    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app


app = create_app()


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
