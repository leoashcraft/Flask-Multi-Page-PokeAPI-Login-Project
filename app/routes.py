from flask import g, render_template, request, redirect, url_for
import requests
from app import app
from .forms import SearchForm, LoginForm, RegisterForm
from .models import User
from flask_login import login_user, logout_user, current_user, login_required

#Routes
@app.route('/', methods=['GET'])
def index():
    form = SearchForm()
    g.form=form
    return render_template('index.html.j2')

@app.route('/register', methods=['GET','POST'])
def register():
    form = SearchForm()
    g.form=form
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        try:
            new_user_data={
                "first_name": form.first_name.data.title(),
                "last_name": form.last_name.data.title(),
                "email": form.email.data.lower(),
                "password": form.password.data
            }
            new_user_object = User()
            new_user_object.from_dict(new_user_data)
        except:
            error_string="There was a problem creating your account. Please try again"
            return render_template('register.html.j2',form=form, error=error_string)
        # Give the user some feedback that says registered successfully 
        return redirect(url_for('login'))

    return render_template('register.html.j2',form=form)

@app.route('/login', methods=['GET','POST'])
def login():
    form = SearchForm()
    g.form=form
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Do login Stuff
        email = form.email.data.lower()
        password = form.password.data
        u = User.query.filter_by(email=email).first()
        print(u)
        if u is not None and u.check_hashed_password(password):
            login_user(u)
            # Give User feeedback of success
            return redirect(url_for('index'))
        else:
            # Give user Invalid Password Combo error
            return redirect(url_for('login'))
    return render_template("login.html.j2", form=form)

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    if current_user is not None:
        logout_user()
        return redirect(url_for('index'))

@app.route('/pokemon', methods=['GET', 'POST'])
@login_required
def pokemon():
    form = SearchForm()
    g.form=form
    if request.method == 'POST' and g.form.validate_on_submit():
        pokemon = form.search.data
        url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}'
        response = requests.get(url)
        if response.ok:
            try:
                data = response.json().get("stats")
                spritedata = response.json()["sprites"]['other']['dream_world'].get("front_default")
            except:
                error_string=f'There is no info for {pokemon}'
                return render_template("pokemon.html.j2", form=form, error=error_string)
            all_stats = []
            for stat in data:
                stat_dict={
                    'poke_statbase':stat['base_stat'],
                    'poke_stateffort':stat['effort'],
                    'poke_statname':stat['stat']['name'],
                }
                all_stats.append(stat_dict)
            return render_template("pokemon.html.j2", form=form, stats=all_stats, sprite=spritedata, pokemon=pokemon.title())
        else:
            error_string="Invalid Pokemon name!"
            return render_template("pokemon.html.j2", form=form, error=error_string)
    return render_template("pokemon.html.j2", form=form)   
#export/set FLASK_APP=app.py
#export/set FLASK_ENV=development
