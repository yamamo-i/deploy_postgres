# coding: utf-8

# import common modules
from fabric.api import sudo, run, env, cd, put
from fabric.decorators import task
from urlparse import urlparse
import time

# import created modules
import common
import munin
import postgres

env.use_ssh_config = True

@task
def startup_postgres(pg_version="9.3.5",
                     package_version="2",
                     # need to rethink default values.
                     os_version="rhel7",
                     architecture="x86_64"):
    ''' install and start postgres task. '''

    # call install postgres task
    postgres.install_postgres_from_local(pg_version, package_version, os_version, architecture)

    # call start postgres process
    postgres.start_postgres(pg_version)

