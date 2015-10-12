from fabric.api import *

@task
def stop_and_clean():
  execute(stop_all)
  execute(clean_storage)
  clean_zk()
  purge_rabbitmq()
  truncate_hbase()
  truncate_solr()
  
@task
def stop_all():
  execute(stop_crawler)

@task
def clean_storage():
  execute(clean_storage_crawler)

@hosts('crawler.gbif-uat.org')
def stop_crawler():
  sudo('cd /home/crap/bin && /home/crap/bin/stop-all.sh', user='crap')
  sudo('sh -c "rm -rf /home/crap/logs/*"', user='crap')
  
@hosts('crawler.gbif-uat.org')
def clean_storage_crawler():
  sudo('sh -c "rm -rf /home/crap/storage/{xml,dwca,results}/*"', user='crap')

@task
def clean_zk():
  local('java -cp /Users/oliver/python/fabric/fabfile/crawlerdev/zookeeper-cleanup.jar org.gbif.util.zookeeper.ZookeeperCleanup /uat_crawler')

@task
def purge_rabbitmq():
  import json
  import urllib2
  import httplib
  import base64

  username = "omeyn"
  password = "omeyn"

  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  headers = {'Authorization': 'Basic %s' % base64string}

  request = urllib2.Request("http://mq.gbif.org:15672/api/queues/%2Fuat")
  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  request.add_header("Authorization", "Basic %s" % base64string)
  data = json.load(urllib2.urlopen(request))

  for queue in data:
    connection = httplib.HTTPConnection('mq.gbif.org:15672')
    url = '/api/queues/%2Fuat/{0}/contents'.format(queue['name'])
    connection.request('DELETE', url, None, headers)
    response = connection.getresponse()
    print('Purging %s: %s, %s' % (queue['name'], response.status, response.reason))

def truncate_hbase():
  local('hbase shell /Users/oliver/python/fabric/fabfile/crawleruat/hbaseclean.rb')

@task
def truncate_solr():
  local('curl -H "Content-Type: text/xml" --data-binary "<delete><query>*:*</query></delete>" http://apps.gbif-uat.org:8081/occurrence-solr/update?commit=true&optimize=true')
  local('curl -H "Content-Type: text/xml" --data-binary "<optimize/>" http://apps.gbif-uat.org:8081/occurrence-solr/update')
      
@task
def start_all():
  execute(start_crawler)

@hosts('crawler.gbif-uat.org')
def start_crawler():
  sudo('sh -c "cd /home/crap/bin && /home/crap/bin/start-all.sh"', user='crap')
  
@task
@hosts('crawler.gbif-uat.org')
def recrawl():
  sudo('sh -c "cd /home/crap/util && /home/crap/util/recrawl.sh"', user='crap')