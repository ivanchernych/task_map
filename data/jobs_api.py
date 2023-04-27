import flask
import datetime
from flask import jsonify, request
from flask_login import current_user
from data import db_session
from jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/job')
def get_job():
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('job', 'team_leader', 'work_size', 'collaborators', 'is_finished'))
                 for item in job]
        }
    )


@blueprint.route('/api/job/<int:job_id>', methods=['GET'])
def get_one_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()
    if not job:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'jobs': job.to_dict(only=(
                'job', 'team_leader', 'work_size', 'collaborators', 'is_finished'))
        }
    )


@blueprint.route('/api/job', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    id_job = db_sess.query(Jobs).filter(Jobs.id == request.json['id']).first()
    if id_job:
        return jsonify({'error': 'Id already exists.'})
    else:
        job = Jobs(
            id=request.json['id'],
            job=request.json['job'],
            team_leader=request.json['team_leader'],
            work_size=request.json['work_size'],
            collaborators=request.json['collaborators'],
            is_finished=request.json['is_finished'],
            start_date=datetime.datetime.now()

        )
        db_sess.add(job)
        db_sess.commit()
        return jsonify({'success': 'OK'})


@blueprint.route('/api/job/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(jobs_id)
    if not job:
        return jsonify({'error': 'Not found'})
    db_sess.delete(job)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/job/<int:jobs_id>', methods=['PUT'])
def edit_jobs(jobs_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()

    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not job:
        return jsonify({'error': 'Not found or Id already exists'})
    elif not all(key in request.json for key in
                 ['id', 'job', 'team_leader', 'work_size', 'collaborators', 'is_finished']):
        return jsonify({'error': 'Bad request'})
    else:
        job.id = request.json['id']
        job.job = request.json['job']
        job.team_leader = request.json['team_leader']
        job.work_size = request.json['work_size']
        job.collaborators = request.json['collaborators']
        job.is_finished = request.json['is_finished']
        db_sess.commit()
        return jsonify({'success': 'OK'})
