from app import app, connection
from mongokit import Document
import datetime


class Todo(Document):
    __database__ = app.config['MONGODB_DB']
    __collection__ = 'todos'
    use_dot_notation = True

    structure = {
        'title': basestring,
        'completed': bool,
        'creator': basestring,
        'created_at': datetime.datetime,
    }
    required_fields = ['title']
    default_values = {
        'completed': False,
        'created_at': datetime.datetime.utcnow
    }


connection.register([Todo])