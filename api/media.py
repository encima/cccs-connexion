import connexion
import logging
import os
from connexion import NoContent
from db import orm_handler, Media
from decorators import access_checks
from werkzeug.utils import secure_filename
import uuid
from flask import send_file
import fleep

db_session = orm_handler.db_session

def get_media(limit=20, search_term=None):
    q = db_session.query(Media)
    if search_term:
        q = q.filter(Media.source_id == search_term)
        # | Media.name.match(search_term, postgresql_regconfig='english') | Media.filetype.match(search_term, postgresql_regconfig='english') | Media.path.match(search_term, postgresql_regconfig='english'))
    return [p.dump() for p in q][:limit]


def get_medium(id=None):
    m = db_session.query(Media).filter(Media.id == id).one_or_none()
    print(m)
    return send_file(m.path) if m is not None else ('Not found', 404)

def get_for_source(id=None, limit=20):
    m = db_session.query(Media).filter(Media.source_id == id)
    return [p.dump() for p in m][:limit]

@access_checks.ensure_key
def upload(id, attachment):
    logging.info('Creating Media ')
    f = connexion.request.files['attachment']
    filename = secure_filename(f.filename)
    uid = uuid.uuid4().hex
    path = os.path.join('./static/uploads/', uid)
    f.save(path)
    with open(path, "rb") as f:
        info = fleep.get(f.read(128))
    print(info.type)
    m = Media(id, path, filename, info.type[0])
    # name = os.path.basename(path)
    db_session.add(m)
    db_session.commit()
    return m.dump(), 201

@access_checks.ensure_key
def put_medium(id, media):
    s = db_session.query(Media).filter(Media.id == id).one_or_none()
    if s is not None:
        logging.info('Updating Media %s..', id)
        s.update(**submission)
    else:
        logging.info('Creating Media %s..', id)
        db_session.add(Media(**media))
    db_session.commit()
    return NoContent, (200 if p is not None else 201)

@access_checks.ensure_key
def delete_medium(id):
    media = db_session.query(Media).filter(Media.id == id).one_or_none()
    if media is not None:
        logging.info('Deleting Media %s..', id)
        os.remove(media.path)
        db_session.query(Media).filter(Media.id == id).delete()
        db_session.commit()
        return media.dump(), 200
    else:
        return NoContent, 404
