# coding=utf-8
from time import sleep
from fabric.api import *

# HBase

@task
@parallel
@roles('all_hbase-masters')
def restart_master():
  run('service hadoop-hbase-master restart')

@task
@parallel
@roles('all_hbase-masters')
def stop_master():
  run('service hadoop-hbase-master stop')

@task
#@parallel
@roles('all_hbase-masters')
def start_master():
  run('service hadoop-hbase-master start')

@task
@parallel
@roles('all_hbase-regionserver')
def restart_regionservers():
  run('service hadoop-hbase-regionserver restart')

@task
@parallel
@roles('all_hbase-regionserver')
def stop_regionservers():
  run('service hadoop-hbase-regionserver stop')

@task
@parallel
@roles('all_hbase-regionserver')
def start_regionservers():
  run('service hadoop-hbase-regionserver start')

@task
def restart_all():
  execute(stop_all)
  execute(start_all)

@task
def stop_all():
  execute(stop_master)
  execute(stop_regionservers)

@task
def start_all():
  execute(start_master)
  sleep(10)
  execute(start_regionservers)
