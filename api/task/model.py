import logging

import sqlalchemy
from api import model
from connexion import NoContent
from db import Media, Submission, Task
from decorators import access_checks
from flask import request
from pony.flask import db_session
from db import Task

Model = Task


def get_tasks(limit, offset, search_term=None):
    return model.get_all(Model, limit, offset, search_term).send()


def get_task_count(search_term=None):
    ms, code = model.get_count(Model, search_term)
    return ms, code


def get_task(tid=None):
    return model.get_one(Model, tid).send()


def create_task(body):
    res, task = model.post(Model, body)
    return res.send()


def create_tasks(body):
    tasks = body
    res = []
    for task in tasks:
        res, t = model.post(Model, task)
        res.append(t.to_dict())
    return res.send()


def update_task(tid, body):
    res, t = model.put(Model, tid, body)
    return res.send()


@access_checks.ensure_owner(Model)
def delete_task(tid):
    return model.delete(Model, tid).send()
