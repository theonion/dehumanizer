import os

from fabric.api import *
from fabric.contrib.project import rsync_project

from contextlib import contextmanager as _contextmanager

env.hosts = ['69.164.217.12']
env.user = 'fabric'
env.webroot = '/www/'
env.projectroot = os.path.join(env.webroot, 'app')
env.activate = 'source bin/activate'


@_contextmanager
def virtualenv():
    with cd(env.projectroot):
        with prefix(env.activate):
            yield


def deploy():
    rsync_project(env.projectroot, local_dir='./', delete=True, exclude=['lib', 'bin', 'build', 'include', 'lib', 'local', 'share', '*.db', '*.pyc', '.git', 'webroot/static'])
    with virtualenv():
        run('pip install -r requirements.txt')
        run('python manage.py collectstatic --settings=dehumanizer.production --noinput')
        run('python manage.py compress --settings=dehumanizer.production')
        run('python manage.py syncdb --settings=dehumanizer.production --noinput')
        run('supervisorctl reload')
