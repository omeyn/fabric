from fabric.api import *

@task
def stop_all():
  execute(stop_bla6)

@hosts('bla6.gbif.org')
def stop_bla6():
  sudo('cd /home/crap/bin && /home/crap/bin/stop-all.sh', user='crap')
  
@hosts('bla6.gbif.org')
def clean_storage_bla6():
  sudo('sh -c "rm -rf /home/crap/storage/{xml,dwca,results}/*"', user='crap')

@task
def clean_zk():
  local('java -cp /Users/oliver/python/fabric/fabfile/crawler/zookeeper-cleanup.jar org.gbif.util.zookeeper.ZookeeperCleanup /prod_crawler/crawls zk1.gbif.org:2181')

@task
def clean_elasticsearch():
  import json
  import urllib2
  import httplib
  data = json.load(urllib2.urlopen('http://b6g8.gbif.org:9200/_status'))
  for index in data['indices']:
    connection = httplib.HTTPConnection('b6g8.gbif.org:9200')
    connection.request('DELETE', '/%s/' % index)
    response = connection.getresponse()
    print('Deleting %s: %s, %s' % (index, response.status, response.reason))

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

  request = urllib2.Request("http://mq.gbif.org:15672/api/queues/%2Fprod")
  base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
  request.add_header("Authorization", "Basic %s" % base64string)
  data = json.load(urllib2.urlopen(request))

  for queue in data:
    connection = httplib.HTTPConnection('mq.gbif.org:15672')
    url = '/api/queues/%2Fprod/{0}/contents'.format(queue['name'])
    connection.request('DELETE', url, None, headers)
    response = connection.getresponse()
    print('Purging %s: %s, %s' % (queue['name'], response.status, response.reason))

@task
def start_all():
  execute(start_bla6)

@task
@hosts('bla6.gbif.org')
def start_cleanup():
  sudo('sh -c "cd /home/crap/bin && /home/crap/bin/start-coordinator-cleanup.sh"', user='crap')

@hosts('bla6.gbif.org')
def start_bla6():
  sudo('sh -c "cd /home/crap/bin && /home/crap/bin/start-all.sh"', user='crap')