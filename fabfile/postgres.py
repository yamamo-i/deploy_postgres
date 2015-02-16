# coding: utf-8

from fabric.api import sudo, run, env, cd, put, settings
from fabric.decorators import task
from urlparse import urlparse
import os

env.use_ssh_config = True

@task
def install_postgres_from_local(pg_version="9.3.5",
                                package_version="2",
                                # need to rethink default values.
                                os_version="rhel7",
                                architecture="x86_64"):
    # TODO need to check argument logic.

    # create version information
    version_array = pg_version.split(".")
    major_version = "".join(version_array[0:2])
    minor_version = version_array[-1]
    package_info  = "".join(["-", package_version, "PGDG.", os_version, ".", architecture, ".rpm"])
    package_dir   = os.path.abspath("./") + "/rpm/pg"

    pg_rpms = [
        "postgresql"+ major_version +"-libs-"+ pg_version + package_info,
        "postgresql"+ major_version +"-"+ pg_version + package_info,
        "postgresql"+ major_version +"-server-"+ pg_version + package_info,
        "postgresql"+ major_version +"-devel-"+ pg_version + package_info
    ]
    run("mkdir -p /tmp/rpm/pg")

    # install postgres package from rpm.
    with cd("/tmp/rpm/pg"):
        for rpm in pg_rpms:
            put( "/".join([ package_dir, os_version, "".join(version_array), rpm]), "/tmp/rpm/pg")
            run("sudo rpm -ivh --replacepkgs " + rpm)

@task
def remove_postgres():
    '''clean PostgreSQL environment'''
    with settings(warn_only=True):
        # stop_postgres if started
        sudo("pkill postgres")
        # remove PGDATA if created
        sudo("rm -rf /var/lib/pgsql/data")
        # remove rpm if installed
        sudo("rpm -e `rpm -qa | grep postgres`")

'''
start postgres process.
'''
@task
def start_postgres(version="9.3.5"):
# TODO set $PG_DATA
# TODO set $PATH
# TODO set directory
# create dynamic setting file that .bash_profile

# TODO The path of pgsql/bin is difference before 9.1.
    major_version = version[0:3]
    sudo("sudo -u postgres mkdir -p /var/lib/pgsql/data")
    sudo("sudo -u postgres /usr/pgsql-"+ major_version +"/bin/initdb --no-locale -D /var/lib/pgsql/data")
    sudo("sudo -u postgres /usr/pgsql-"+ major_version +"/bin/pg_ctl start -w -D /var/lib/pgsql/data")


'''
deploy PostgreSQL between get rpm_package and install from internet.
This method is test code and can't apply mulit version deployment.
'''
def install_postgres_from_web():
    pg_rpms = [
        "http://yum.postgresql.org/9.3/redhat/rhel-7-x86_64/postgresql93-libs-9.3.5-2PGDG.rhel7.x86_64.rpm",
        "http://yum.postgresql.org/9.3/redhat/rhel-7-x86_64/postgresql93-9.3.5-2PGDG.rhel7.x86_64.rpm",
        "http://yum.postgresql.org/9.3/redhat/rhel-7-x86_64/postgresql93-server-9.3.5-2PGDG.rhel7.x86_64.rpm",
        "http://yum.postgresql.org/9.3/redhat/rhel-7-x86_64/postgresql93-devel-9.3.5-2PGDG.rhel7.x86_64.rpm"
    ]
    run("mkdir -p ~/rpm/pg")
    
    with cd("~/rpm/pg"):
        for rpm in pg_rpms:
            run("wget " + rpm)
            run("sudo rpm -ivh --replacepkgs " + urlparse(rpm).path.split("/")[-1])

