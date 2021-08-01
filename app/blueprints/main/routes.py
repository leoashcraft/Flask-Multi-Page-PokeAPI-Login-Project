from flask import g, render_template, request, flash
import requests
from .forms import SearchForm
from flask_login import login_required
from .import bp as main

#Routes
@main.route('/', methods=['GET'])
def index():
    form = SearchForm()
    g.form=form
    return render_template('index.html.j2')

@main.route('/pokemon', methods=['GET', 'POST'])
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
                flash('There is no info for {pokemon}', 'warning')
                return render_template("pokemon.html.j2", form=form)
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
            flash('Invalid Pokemon name!', 'danger')
            return render_template("pokemon.html.j2", form=form)
    return render_template("pokemon.html.j2", form=form)   
#export/set FLASK_APP=app.py
#export/set FLASK_ENV=development
