from fabric.api import *
from awsfabrictasks.decorators import ec2instance
from fabtools import require
from fabtools.python import virtualenv
# globals
env.use_ssh_config = False
env.hosts = ['54.209.245.159']
env.user = 'ubuntu'

REPOS = '$HOME/repos/'

REMOTE_URL = 'https://github.com/syllog1sm/piegin.git'

@task
def provision():
    #run('sudo apt-get update')
    #run('sudo apt-get install python-pip')
    require.deb.packages(('python-pip', 'python-dev', 'build-essential'))
    require.deb.packages(('libxml2-dev', 'libxslt1-dev'))
    require.deb.packages(('nginx', 'supervisor'))
    require.deb.package('git')
    require.deb.package('libpq-dev')
    require.python.pip()
    require.files.directories((REPOS, '/var/www'), use_sudo=True)

    require.git.command()

    with cd(REPOS):
        require.git.working_copy(REMOTE_URL)
        run('pip install -r requirements.txt')


####################
# Import awsfab tasks
#####################
from awsfabrictasks.ec2.tasks import *
from awsfabrictasks.regions import *
from awsfabrictasks.conf import *
