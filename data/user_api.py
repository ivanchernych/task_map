import flask
from flask import jsonify, request
from data import db_session
from static.users import User

blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user')
def get_user():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                                    'hashed_password', 'modified_date', 'city_from'))
                 for item in user]
        }
    )


@blueprint.route('/api/user/<int:user_id>', methods=['GET'])
def get_one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': user.to_dict(only=('surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                                        'hashed_password', 'modified_date', 'city_from'))
        }
    )


@blueprint.route('/api/user', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                  'password', 'modified_date', 'city_from']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    id_user = db_sess.query(User).filter(User.id == request.json['id']).first()
    if id_user:
        return jsonify({'error': 'Id already exists.'})
    else:
        user = User(
            id=request.json['id'],
            surname=request.json['surname'],
            name=request.json['name'],
            age=request.json['age'],
            position=request.json['position'],
            speciality=request.json['speciality'],
            address=request.json['speciality'],
            email=request.json['email'],
            modified_date=request.json['modified_date'],
            city_from=request.json['city_from']

        )
        user.set_password(request.json['password'])
        db_sess.add(user)
        db_sess.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['DELETE'])
def delete_jobs(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/user/<int:user_id>', methods=['PUT'])
def edit_jobs(user_id):
    db_sess = db_session.create_session()
    job = db_sess.query(User).filter(User.id == user_id).first()

    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not job:
        return jsonify({'error': 'Not found or Id already exists'})
    elif not all(key in request.json for key in
                 ['id', 'surname', 'name', 'age', 'position', 'speciality', 'address', 'email',
                  'password', 'modified_date, city_from']):
        return jsonify({'error': 'Bad request'})
    else:
        job.id = request.json['id']
        job.surname = request.json['surname']
        job.name = request.json['name']
        job.age = request.json['age']
        job.position = request.json['position']
        job.speciality = request.json['speciality']
        job.address = request.json['address']
        job.email = request.json['email']
        job.password = request.json['password']
        job.modified_date = request.json['modified_date']
        job.city_from = request.json['city_from']
        db_sess.commit()
        return jsonify({'success': 'OK'})
