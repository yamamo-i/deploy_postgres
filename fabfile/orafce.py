# coding: utf-8

from fabric.api import sudo, run, env, cd, put, settings, shell_env
from fabric.decorators import task
import os

env.use_ssh_config = True

@task
def install(orafce_version="3.0.7",
            package_version="1",
            pg_version="9.3.5",
            os_version="rhel7",
            architecture="x86_64"):
    ''' install orafce'''
    # ex) orafce93-3.0.7-1.rhel7.x86_64.rpm
    # create version information
    version_array = pg_version.split(".")
    major_version = "".join(version_array[0:2])
    working_directory = "/tmp/rpm/orafce"
    package_dir = os.path.abspath("./") + "/rpm/pg_tools/orafce/"

    orafce_rpms = [
        "orafce" + major_version + "-" + orafce_version + "-" + package_version + "." + os_version + "." + architecture + ".rpm"
    ]
    run("mkdir -p %s" % working_directory)

    with cd(working_directory):
        for rpm in orafce_rpms:
            put(package_dir + rpm, working_directory)
            run("sudo rpm -ivh --replacepkgs " + rpm)

    # cleanup tmp directory
    run("rm -rf %s" % working_directory)

@task
def test(orafce_version="3.0.7",
         pg_version="9.3.5",
         pg_user="postgres",
         testdb="testdb"):
    ''' test orafce'''
    # must installed software "gcc, bison, flex"
    # execute command "sudo yum install -y gcc bison flex"

    # TODO need to switch branch in local node.

    # create information
    orafce_source_path = os.path.abspath("./") + "/pg_tools/orafce"
    working_directory = "/tmp/pg_tools/"
    version_array = pg_version.split(".")
    pg_major_version = ".".join(version_array[0:2])
    pg_bin_path = "/usr/pgsql-%s/bin" % pg_major_version

    with shell_env(PATH="%s:$PATH" % pg_bin_path, PGUSER=pg_user, PGDATABASE=testdb):
        # create extension and test environment
        with settings(warn_only=True):
            run("dropdb %s -U %s" % (testdb, pg_user))
            run("rm -rf %s" % working_directory)
            run("rm -rf %s")
        ## create testdb
        run("createdb %s -U %s" % (testdb, pg_user))
        ## create extension
        run("psql %s %s -c 'CREATE EXTENSION orafce'" % (testdb, pg_user))

        # put orafce source
        run("mkdir -p %s" % working_directory)
        put(orafce_source_path, working_directory)

        # make installcheck
        with cd(working_directory + "orafce"):
            run("make")
            run("make installcheck")

        # remove orafce test environment
        with settings(warn_only=True):
            run("psql %s %s -c 'DROP EXTENSION orafce'" % (testdb, pg_user))
            run("rm -rf %s" % working_directory)
            run("dropdb %s -U %s" % (testdb, pg_user))

@task
def uninstall():
    ''' uninstall orafce'''
    with settings(warn_only=True):
        sudo("rpm -e `rpm -qa | grep orafce`")

