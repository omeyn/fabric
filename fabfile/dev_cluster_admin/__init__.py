# coding=utf-8
from time import sleep
from fabric.api import *

# fix ntp so that it can be queried
@task
@parallel
@roles('c2all')
def fix_ntp():
  run("sed -i 's/restrict default nomodify notrap noquery/restrict default nomodify notrap/g' /etc/ntp.conf")
  run("service ntpd restart")

# Ganglia
@task
@parallel
@roles('c2all')
def stop_gmond():
  run('service gmond stop')
  
@task
@parallel
@roles('c2all')
def start_gmond():
  run('chkconfig gmond on')
  run('service gmond start')

@task
@parallel
@roles('c2all')
def add_appdev_mount():
  run("echo 'appdev		-nolock		transit.gbif.org:/mnt/large/appdev' >> /etc/auto.mnt")
  run('service autofs restart')
  
@task
@parallel
@roles('c2all')
def stop_autofs():
  run('service autofs stop')
  
@task
@parallel
@roles('c2all')
def start_autofs():
  run('service autofs start')
  
@task
@parallel
@roles('c2all')
def yumupdate():
  run('yum -y update')
  
@task
@parallel
@roles('c2slaves')
def yumupdate_slaves():
  run('yum -y update')

@task
@parallel
@roles('c2all')
def reboot():
  run('shutdown -r now')
  
@task
@parallel
@roles('c2all')
def add_uat_mount():
  # run("mv /etc/auto.mnt /etc/auto.mnt.old")
  # run("echo 'prod   -nolock   transit.gbif.org:/mnt/large/prod' > /etc/auto.mnt")
  # run("echo 'uat   -nolock   transit.gbif.org:/mnt/large/uat' >> /etc/auto.mnt")
  # run("echo 'dev   -nolock   transit.gbif.org:/mnt/large/dev' >> /etc/auto.mnt")
  # run('service autofs restart')
  run("rm -f /etc/auto.mnt.old")
  run("cd /mnt/auto/uat/occurrence-download && ls /mnt/auto/uat/occurrence-download")

@task
@parallel
@roles('c2all')
def restart_cloudera_agent():
  run('service cloudera-scm-agent restart')
  
@task
@parallel
@roles('c2all')
def stop_cloudera_agent():
  run('service cloudera-scm-agent stop')
  
@task
@parallel
@roles('c2all')
def remove_java6():
  run('rpm -e jdk-1.6.0_31-fcs.x86_64')

@task
@parallel
@roles('c2all')
def switch_to_java8():
  run('alternatives --set java /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.45-28.b13.el6_6.x86_64/jre/bin/java')
  
@task
@parallel
@roles('c2all')
def install_java8():
  run('yum -y install java-1.8.0-openjdk-src java-1.8.0-openjdk-devel')
    
@task
@parallel
@roles('c2all')
def add_java7_dev():
  run('yum -y install java-1.7.0-openjdk-devel')
  
@task
@parallel
@roles('c2all')
def copy_jts():
  run('mkdir /opt/cloudera/auxjar')
  run('cd /opt/cloudera/auxjar && hadoop fs -get /solr/auxjar/jts-1.13.jar')

@task
@roles('c2all')
def check_and_set_kernel_params():
  # run('cat /etc/rc.local')
  run('cat /sys/kernel/mm/redhat_transparent_hugepage/defrag')
  run('echo 360448 > /proc/sys/vm/min_free_kbytes')
  run('echo 1 > /proc/sys/vm/zone_reclaim_mode')
  run('echo never > /sys/kernel/mm/redhat_transparent_hugepage/defrag')
  run('cat /sys/kernel/mm/redhat_transparent_hugepage/defrag')
  
#@task
@roles('c2all')
def add_sysctl_params():
  run('echo "vm.min_free_kbytes = 360448" >> /etc/sysctl.conf')
  run('echo "vm.zone_reclaim_mode = 1" >> /etc/sysctl.conf')
  
@task
@parallel
@roles('c2all')
def set_swappiness():
  run("sed -i 's/vm.swappiness = 1/vm.swappiness = 0/g' /etc/sysctl.conf")
  run("sysctl vm.swappiness=0")
  run("swapoff -a")
  run("swapon -a")
    
@task
@parallel
@roles('c2slaves')
def format_dn_disks():
  run('umount /dev/sda3')
  run('mkfs.ext4 -b 4096 -I 256 -m 0 /dev/sda3')
  run('mount /dev/sda3')
  run('umount /dev/sdb1')
  run('mkfs.ext4 -b 4096 -I 256 -m 0 /dev/sdb1')
  run('mount /dev/sdb1')
  run('umount /dev/sdc1')
  run('mkfs.ext4 -b 4096 -I 256 -m 0 /dev/sdc1')
  run('mount /dev/sdc1')
  run('umount /dev/sdd1')
  run('mkfs.ext4 -b 4096 -I 256 -m 0 /dev/sdd1')
  run('mount /dev/sdd1')
  run('umount /dev/sde1')
  run('mkfs.ext4 -b 4096 -I 256 -m 0 /dev/sde1')
  run('mount /dev/sde1')
  run('umount /dev/sdf1')
  run('mkfs.ext4 -b 4096 -I 256 -m 0 /dev/sdf1')
  run('mount /dev/sdf1')

@task
@parallel
@roles('c2masters')
def format_nn_disks():
  run('umount /dev/sda3')
  run('mkfs.ext4 -b 4096 -I 256 -m 0 /dev/sda3')
  run('mount /dev/sda3')
  run('umount /dev/sdb1')
  run('mkfs.ext4 -b 4096 -I 256 -m 0 /dev/sdb1')
  run('mount /dev/sdb1')