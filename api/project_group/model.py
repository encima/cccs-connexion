from connexion import NoContent
from db import Comment, utils, User, Project, ProjectGroup
from decorators import access_checks
from flask import request
import logging
from api import model

from pony.flask import db_session

Model = ProjectGroup


def get_project_groups(limit=100, offset=0, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()


def get_project_group(pid=None):
    return model.get_one(Model, pid).send()


@db_session
def create_project_group(body):
    group = body
    user = utils.get_user(request, db_session)
    project["owned_by"] = user.id
    res, _ = model.post(Model, project)
    return res.send()


def update_project_group(pid, body):
    res, _ = model.put(Model, pid, body)
    return res.send()


@db_session
@access_checks.ensure_owner(Model)
def delete_project_group(pid):
    return model.delete(Model, pid).send()
