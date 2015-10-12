# coding=utf-8

import hbase, test, crawlerdev, crawler, crawleruat, prod_cluster_admin, dev_cluster_admin, prodreproc, uatreproc, home_cluster_admin

from fabric.api import env, roles, run, put

env.use_ssh_config = True
env.sudo_user = 'root'
env.user = 'root'

env.roledefs['homemasters'] = ['master1.home', 'master2.home', 'master3.home']
env.roledefs['homeslaves'] = ['slave1.home', 'slave2.home', 'slave3.home', 'slave4.home', 'slave5.home', 'slave6-vh.home', 'slave7-vh.home', 'slave8-vh.home', 'slave9-vh.home']
env.roledefs['homeall'] = env.roledefs['homemasters'] + env.roledefs['homeslaves']

env.roledefs['c2masters'] = ['c1n1.gbif.org', 'c1n2.gbif.org', 'c1n3.gbif.org']
env.roledefs['c2slaves'] = ['c2n1.gbif.org', 'c2n2.gbif.org', 'c2n3.gbif.org', 'bantha.gbif.org']
env.roledefs['c2gateways'] = ['devgateway-vh.gbif.org']
env.roledefs['c2all'] = env.roledefs['c2masters'] + env.roledefs['c2slaves'] + env.roledefs['c2gateways']

env.roledefs['c4masters'] = ['prodmaster1-vh.gbif.org', 'prodmaster2-vh.gbif.org', 'prodmaster3-vh.gbif.org']
env.roledefs['c4slaves'] = ['c4n1.gbif.org', 'c4n2.gbif.org', 'c4n3.gbif.org', 'c4n4.gbif.org', 'c4n5.gbif.org', 'c4n6.gbif.org', 'c4n7.gbif.org', 'c4n8.gbif.org', 'c4n9.gbif.org', 'c4n10.gbif.org', 'c4n11.gbif.org', 'c4n12.gbif.org']
env.roledefs['c4solr']=['prodsolr1-vh.gbif.org', 'prodsolr2-vh.gbif.org', 'prodsolr3-vh.gbif.org']
env.roledefs['c4gateways'] = ['prodgateway-vh.gbif.org']
env.roledefs['c4all'] = env.roledefs['c4masters'] + env.roledefs['c4slaves'] + env.roledefs['c4gateways'] + env.roledefs['c4solr']

env.roledefs['prod_reproc'] = ['b11g9.gbif.org','b7g4.gbif.org','b8g1.gbif.org','b14g2.gbif.org','b16g3.gbif.org']
env.roledefs['uat_reproc'] = ['bla9.gbif.org','b11g9.gbif.org','kyle.gbif.org','oliver.gbif.org','ecat-dev.gbif.org']

