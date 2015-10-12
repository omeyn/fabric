# coding=utf-8
from time import sleep
from fabric.api import *

# fix ntp so that it can be queried
@task
@parallel
@roles('c4all')
def fix_ntp():
  run("sed -i 's/restrict default nomodify notrap noquery/restrict default nomodify notrap/g' /etc/ntp.conf")
  run("service ntpd restart")
  
@task
@roles('c4all')
def check_ntp():
  run("ntpdc -np")
  
# Ganglia
@task
@parallel
@roles('c4all')
def stop_gmond():
  run('service gmond stop')
  
@task
@parallel
@roles('c4all')
def start_gmond():
  run('service gmond start')
  
@task
@parallel
@roles('c4all')
def restart_gmond():
  run('service gmond restart')
  
@task
@parallel
@roles('c4')
def add_prod_mount():
#	run("sed -n '$!p' /etc/auto.mnt > /etc/tmp.txt && mv -f /etc/tmp.txt /etc/auto.mnt")
  run("echo 'prod		-nolock		transit.gbif.org:/mnt/large/prod' >> /etc/auto.mnt")
  run('service autofs restart')
  
@task
@parallel
@roles('c4')
def add_appdev_mount():
  run("echo 'appdev		-nolock		transit.gbif.org:/mnt/large/appdev' >> /etc/auto.mnt")
  run('service autofs restart')
  
@task
@parallel
@roles('c4')
def prod_unmount():
  run('service autofs stop')
  
@task
@parallel
@roles('c4')
def prod_mount():
  run('service autofs start')

@task
@parallel
@roles('c4')
def yumupdate():
  run('yum -y update')
  
@task
@parallel
@roles('c4')
def reboot():
  run('shutdown -r now')

@task
@parallel
@roles('newprodmasters')
def masteryumupdate():
  run('yum -y update')

@task
@parallel
@roles('newprodmasters')
def masterreboot():
  run('shutdown -r now')
  
@task
@parallel
@roles('c4')
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
@roles('c4all')
def switch_to_java8():
  run('alternatives --set java /usr/lib/jvm/jre-1.8.0-openjdk.x86_64/bin/java')
  
@task
@parallel
@roles('c4')
def switch_to_java7():
  run('alternatives --set java /usr/lib/jvm/jre-1.7.0-openjdk.x86_64/bin/java')

@task
@parallel
@roles('c4')
def switch_to_java6():
  run('alternatives --set java /usr/lib/jvm/jre-1.6.0-sun/bin/java')
  
@task
@parallel
@roles('c4')
def remove_java6():
  run('rpm -e jdk-1.6.0_31-fcs.x86_64')
  run('rpm -e java-1.6.0-sun-1.6.0.45-1jpp.el6_gbif.x86_64')  

@task
@parallel
@roles('c4all')
def install_java8():
  run('yum -y install java-1.8.0-openjdk-src java-1.8.0-openjdk-devel')

@task
@parallel
@roles('c4all')
def switch_to_java8():
  run('alternatives --set java /usr/lib/jvm/java-1.8.0-openjdk-1.8.0.45-28.b13.el6_6.x86_64/jre/bin/java')

@task
@parallel
@roles('c4')
def install_jdk_dev_src():
  run('yum -y install java-1.7.0-openjdk-src java-1.7.0-openjdk-devel')

@task
@parallel
@roles('c4')
def copy_jts():
  # run('mkdir /opt/cloudera/auxjar')
  run('cd /opt/cloudera/auxjar && hadoop fs -get /olivertmp/jts-1.13.jar')

@task
@parallel
@roles('c4slaves')
def distribute_jts():
  put('/Users/oliver/java/zips/jts-1.13.jar', '/opt/cloudera/parcels/CDH/lib/solr/webapps/solr/WEB-INF/lib/')
  
@task
@roles('c4')
def ls_jts():
  run('ls /opt/cloudera/auxjar')
  
@task
@parallel
@roles('c4all')
def restart_cloudera_agent():
  run('service cloudera-scm-agent restart')

@task
@roles('newprodmasters')
def check_and_set_kernel_params():
  # run('cat /etc/rc.local')
  run('cat /sys/kernel/mm/redhat_transparent_hugepage/defrag')
  run('echo 360448 > /proc/sys/vm/min_free_kbytes')
  run('echo 1 > /proc/sys/vm/zone_reclaim_mode')
  run('echo never > /sys/kernel/mm/redhat_transparent_hugepage/defrag')
  run('cat /sys/kernel/mm/redhat_transparent_hugepage/defrag')
  
@task
@roles('newprodmasters')
def add_sysctl_params():
  run('echo "vm.min_free_kbytes = 360448" >> /etc/sysctl.conf')
  run('echo "vm.zone_reclaim_mode = 0" >> /etc/sysctl.conf')
  run('echo "vm.swappiness = 0" >> /etc/sysctl.conf')
  run("swapoff -a")
  run("swapon -a")

@task
@roles('newprodmasters')
def clean_tmp():
  run('rm -Rf /tmp/scm_prepare*')
  run('rm -Rf /tmp/.scm_prepare*')
  run('rm -Rf /tmp/cmflistener*')
  
@task
@parallel
@roles('c4')
def check_for_jts():
  run('ls /opt/cloudera/parcels/SOLR/lib/solr/server/webapps/solr/WEB-INF/lib/jts-1.13.jar')

@task
@parallel
@roles('c4')
def set_swappiness():
  run("sed -i 's/vm.swappiness = 1/vm.swappiness = 0/g' /etc/sysctl.conf")
  run("sysctl vm.swappiness=0")
  run("swapoff -a")
  run("swapon -a")
  
@task
def clean_elasticsearch_logs():
  import json
  import urllib2
  import httplib
  from datetime import datetime, timedelta

  print('Deleting logstash indices that are more than 1 month old')
  today = datetime.now()
  lastMonth = monthdelta(today, -1)
  # twoMonthsAgo = monthdelta(today, -2)

  data = json.load(urllib2.urlopen('http://b6g8.gbif.org:9200/_status'))
  for index in data['indices']:
    if index.find(formatDateString(today.year, today.month)) < 0 and index.find(formatDateString(lastMonth.year, lastMonth.month)) < 0:
    #and index.find(formatDateString(twoMonthsAgo.year, twoMonthsAgo.month)) < 0:
      connection = httplib.HTTPConnection('b6g8.gbif.org:9200')
      connection.request('DELETE', '/%s/' % index)
      response = connection.getresponse()
      print('Deleting index %s: %s, %s' % (index, response.status, response.reason))

def formatDateString(year, month):
  dateString = str(year) + '.'
  if month < 10:
    dateString = dateString + str(0)
  dateString = dateString + str(month)
  return dateString
  
def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)