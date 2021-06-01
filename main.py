import json
import logging
import os
import uuid

from PIL import Image
import flask

import config
import models
import utils


@config.app.route(r'/project', methods=['GET'])
def list_projects():
    project_list = [proj.to_dict() for proj in models.Project.query.filter_by(
        active=True)]
    return json.dumps(project_list, indent=4, sort_keys=True, default=str)


@config.app.route(r'/project/<project_id>', methods=['GET'])
def get_project(project_id):
    if not project_id:
        return flask.abort(404, description=f'Project {project_id} not found.')
    project = models.Project.query.get(project_id)
    if project is None or not project.active:
        return flask.abort(404, description=f'Project {project_id} not found.')
    return project.to_json()


@config.app.route(r'/project', methods=['POST'])
def create_project():
    project_dict = flask.request.form.to_dict()
    if not project_dict:
        return flask.abort(403, description=f'Project playload empty.')
    utils.clean_columns(project_dict, {'name', 'active'})

    project = models.Project.from_dict(project_dict)
    config.db.session.add(project)
    config.db.session.commit()
    return (f'{project.name} created.', 200)


@config.app.route(r'/project', methods=['PATCH'])
def update_project():
    project_dict = flask.request.form.to_dict()

    utils.clean_columns(project_dict, {'id', 'name'})
    project_id = project_dict.get('id')
    project = models.Project.query.get(project_id)
    if project is None or not project.active:
        return flask.abort(404, description=f'Project {project_id} not found.')
    project.active = project_dict.get('active', True)
    project.name = project_dict.get('name', True)

    config.db.session.add(project)
    config.db.session.commit()
    return (f'{project.name} updated.', 200)


@config.app.route(r'/project/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    project = models.Project.query.get(project_id)
    if project is None or not project.active:
        return flask.abort(404, description=f'Project {project_id} not found.')

    project.active = False
    config.db.session.add(project)
    config.db.session.commit()
    return (f'Project {project_id} deleted.', 200)


@config.app.route(r'/floorplan', methods=['GET'])
def list_floorplan():
    floorplan_list = [fp.to_dict(exclude=('file_id',))
                      for fp in models.Floorplan.query.filter_by(active=True)]
    return json.dumps(floorplan_list, indent=4, sort_keys=True, default=str)


@config.app.route(r'/floorplan/<floorplan_id>', methods=['GET'])
def get_floorplan(floorplan_id):
    if not floorplan_id:
        return flask.abort(
            404, description=f'Floorplan {floorplan_id} not found.')
    floorplan = models.Floorplan.query.get(floorplan_id)
    if floorplan is None or not floorplan.active:
        return flask.abort(
            404, description=f'Floorplan {floorplan_id} not found.')
    floorplan_dict = floorplan.to_dict(exclude=('file_id'))
    floorplan_dict['thumbs'] = [
        t.to_dict() for t in floorplan.thumbs if t.active]
    return json.dumps(floorplan_dict)


def _add_thumbs_to_floorplan(original_file, floorplan, sizes):
    with Image.open(original_file) as image:
        format = image.format
        for size in sizes:
            thumb_id = str(uuid.uuid4())
            image.thumbnail(size)
            path = os.path.join(config.FLOORPLAN_IMG_DIR, thumb_id)
            image.save(path, format)
            floorplan.thumbs.append(models.Thumb(thumb_id=thumb_id))


@config.app.route(r'/floorplan', methods=['POST'])
def create_floorplan():
    floorplan_dict = flask.request.form.to_dict()
    utils.clean_columns(floorplan_dict, {'project_id',})

    original_file = flask.request.files.get('original')
    if not original_file:
        return flask.abort(
            404, description='Floorplan attachment not found.')

    floorplan_dict['name'] = original_file.filename
    file_id = str(uuid.uuid4())
    floorplan_dict['file_id'] = file_id

    filepath = os.path.join(config.FLOORPLAN_IMG_DIR, file_id)
    original_file.save(filepath)
    floorplan = models.Floorplan.from_dict(floorplan_dict)
    _add_thumbs_to_floorplan(
        original_file, floorplan, ((100, 100), (2000, 2000)))

    config.db.session.add(floorplan)
    config.db.session.commit()
    return (f'{floorplan.name} created.', 200)


@config.app.route(r'/floorplan', methods=['PATCH'])
def update_floorplan():
    floorplan_dict = flask.request.form.to_dict()
    utils.clean_columns(floorplan_dict, {'id', 'project_id', 'name'})

    floorplan_id = floorplan_dict.get('id')
    floorplan = models.Floorplan.query.get(floorplan_id)
    if floorplan is None or not floorplan.active:
        return flask.abort(
            404, description=f'Floorplan {floorplan_id} not found.')

    original_file = flask.request.files.get('original')
    # Is this a different file.
    if original_file and floorplan.name != original_file.filename:
        floorplan_dict['name'] = original_file.filename
        file_id = str(uuid.uuid4())
        floorplan_dict['file_id'] = file_id
        filepath = os.path.join(config.FLOORPLAN_IMG_DIR, file_id)
        original_file.save(filepath)
        for thumb in floorplan.thumbs:
            thumb.active = False
        _add_thumbs_to_floorplan(
            original_file, floorplan, ((100, 100), (2000, 2000)))

    project_id = floorplan_dict.get('project_id')
    if project_id:
        floorplan.project_id = project_id
    name = floorplan_dict.get('name')
    if name:
        floorplan.name = name
    config.db.session.add(floorplan)
    config.db.session.commit()
    return (f'{floorplan.name} updated.', 200)


@config.app.route(r'/floorplan/<floorplan_id>', methods=['DELETE'])
def delete_floorplan(floorplan_id):
    floorplan_id = int(florpolan_id)
    floorplan = models.Floorplan.query.get(floorplan_id)
    if floorplan is None or not floorplan.active:
        return flask.abort(
            404, description=f'Floorplan {floorplan_id} not found.')

    models.Floorplan.query.filter(models.Floorplan.id==floorplan_id).join(
        'thumbs').update({
            models.Floorplan.active: False,
            models.Thumb.active: False
        })
    return (f'{floorplan.name} deleted.', 200)


@config.app.route(r'/floorplan/file/<floorplan_id>', methods=['GET'])
def get_file(floorplan_id):
    if not floorplan_id:
        return flask.abort(
            404, description=f'Floorplan {floorplan_id} not found.')
    floorplan = models.Floorplan.query.get(floorplan_id)
    if floorplan is None or not floorplan.active:
        return flask.abort(
            404, description=f'Floorplan {floorplan_id} not found.')
    return flask.send_from_directory(
        config.FLOORPLAN_IMG_DIR, floorplan.file_id, as_attachment=True)


@config.app.route(r'/floorplan/<floorplan_id>/thumb/<thumb_id>', methods=['GET'])
def get_thumb(floorplan_id, thumb_id):
    if not floorplan_id or not thumb_id:
        return flask.abort(404, description=f'Thumb not found.')
    floorplan_thumb = models.Thumb.query.filter_by(
        id=thumb_id, active=True).join('floorplan').filter(
            models.Floorplan.id==floorplan_id, models.Floorplan.active.is_(
                True)).one_or_none()
    if floorplan_thumb is None:
        return flask.abort(404, description=f'Thumb not found.')
    return flask.send_from_directory(
        config.FLOORPLAN_IMG_DIR, floorplan_thumb.thumb_id)


if __name__ == '__main__':
    if not utils.db_exists():
        logging.info('Creating database.')
        config.db.create_all()
    if not utils.floorplan_dir_exists():
        logging.info('Creating floorlan dir.')
        utils.create_floorplan_dir()
    config.app.run(debug=True)
