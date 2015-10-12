# coding=utf-8
from time import sleep
from fabric.api import *

# fix ntp so that it can be queried
@task
@parallel
@roles('homeall')
def fix_ntp():
  # run("sed -i 's/restrict default nomodify notrap noquery/restrict default nomodify notrap/g' /etc/ntp.conf")
  run("service ntpd restart")

# Ganglia
@task
@parallel
@roles('homeall')
def stop_gmond():
  run('service gmond stop')
  
@task
@parallel
@roles('homeall')
def start_gmond():
  run('chkconfig gmond on')
  run('service gmond start')

@task
@parallel
@roles('homeall')
def yumupdate():
  run('yum -y update')
  
@task
@parallel
@roles('homeslaves')
def yumupdate_slaves():
  run('yum -y update')

@task
@parallel
@roles('homeall')
def reboot():
  run('shutdown -r now')

@task
@parallel
@roles('homeslaves')
def reboot_slaves():
  run('shutdown -r now')

@task
@parallel
@roles('homeall')
def restart_cloudera_agent():
  run('service cloudera-scm-agent restart')
  
@task
@parallel
@roles('homeall')
def stop_cloudera_agent():
  run('service cloudera-scm-agent stop')

@task
@parallel
@roles('homeall')
def switch_to_java8():
  run('alternatives --set java /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.45-28.b13.el6_6.x86_64/jre/bin/java')
  
@task
@parallel
@roles('homeall')
def install_java8():
  run('yum -y install java-1.8.0-openjdk-src java-1.8.0-openjdk-devel')
    
@task
@parallel
@roles('homeall')
def add_java7_dev():
  run('yum -y install java-1.7.0-openjdk-devel')
  
@task
@parallel
@roles('homeall')
def copy_jts():
  run('mkdir /opt/cloudera/auxjar')
  run('cd /opt/cloudera/auxjar && hadoop fs -get /solr/auxjar/jts-1.13.jar')
  
@task
@parallel
@roles('homeslaves')
def fix_dfs():
  run('chown hdfs.hadoop /dfs/dn')
  run('chown hdfs.hadoop /dfs/dn2')

# @task
# @parallel
# @roles('homeslaves')
# def rebuild_sdb1():
#
# umount /home
# e2fsck -f /dev/mapper/vg_slave1-lv_home
# resize2fs /dev/mapper/vg_slave1-lv_home 100G
# lvreduce -L 120G /dev/mapper/vg_slave1-lv_home
# resize2fs /dev/mapper/vg_slave1-lv_home
# vgchange -a y
# mount /home
#
# # slave2 has disks backwards
# pvmove /dev/sdb1
# vgreduce vg_slave1 /dev/sdb1
# fdisk /dev/sdb
# mkfs.ext4 -b 4096 -I 256 -m 0 /dev/sdb1
#
# add to fstab
# /dev/sdb1    /dfs/dn      ext4  defaults  1 2