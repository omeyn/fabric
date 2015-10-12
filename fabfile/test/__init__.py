# coding=utf-8

from fabric.api import *

@task
@hosts('crawler.gbif-uat.org')
def test():
  sudo('ls /home/crap', user='crap')
