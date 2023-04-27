import flask
from data import db_session, user_api
from requests import get
from getting_coordinates import generate_city

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    app.register_blueprint(user_api.blueprint)
    app.run()


@app.route('/<int:user_id>')
@app.route('/users_show/<int:user_id>')
def user_show(user_id):
    url = f'http://localhost:5000/api/user/{user_id}'
    json = get(url).json()
    name_surname = json['users']['name'] + ' ' + json['users']['surname']
    city = json['users']['city_from']
    response = generate_city(city)
    if response:
        map_file = "static/img/map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)
    return flask.render_template('base.html', title='map', name=name_surname)


if __name__ == '__main__':
    main()
