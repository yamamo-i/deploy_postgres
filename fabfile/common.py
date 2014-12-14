# coding: utf-8

from fabric.api import sudo, run, env, cd, put
from fabric.decorators import task

env.use_ssh_config = True

@task
def install_min_pkg():
    sudo("yum -y install git zsh tmux")
@task
def enable_epel():
    sudo("yum -y  install epel-release")


