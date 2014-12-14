# coding: utf-8

from fabric.api import sudo, run, env, cd, put
import os

env.use_ssh_config = True

def install_munin_from_web():
    sudo("yum install -y --skip-broken munin munin-node")

def install_munin_from_local():

    package_dir= os.path.abspath("./") + "/rpm/munin/"
    munin_pkgs = [
        "munin-common-2.0.24-1.el7.noarch.rpm",
        "munin-node-2.0.24-1.el7.noarch.rpm",
        "munin-2.0.24-1.el7.src.rpm"
    ]
    run("mkdir -p /tmp/munin")

    with cd("/tmp/munin"):
            for pkg in munin_pkgs:
                put( package_dir + pkg, "/tmp/munin")
                run("sudo rpm -ivh --replacepkgs " + pkg)


