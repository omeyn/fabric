from fabric.api import *

@task
@parallel
@roles('uat_reproc')
def stop():
  sudo('sh -c "cd /home/crap/uat_reproc/bin && /home/crap/uat_reproc/bin/stop-processors.sh"')

@task
@parallel
@roles('uat_reproc')
def start_verbatim():
  sudo('sh -c "cd /home/crap/uat_reproc/bin && /home/crap/uat_reproc/bin/start-processor-verbatim.sh"')

@task
@parallel
@roles('uat_reproc')
def start_interp():
  sudo('sh -c "cd /home/crap/uat_reproc/bin && /home/crap/uat_reproc/bin/start-processor-interpreted.sh"')
  
@task
@parallel
@roles('uat_reproc')
def setup_dirs():
  sudo('sh -c "chown -R crap.crap /home/crap/uat_reproc"')

@task
@parallel
@roles('uat_reproc')
def check_ps():
  sudo('sh -c "ps aux | grep jav | grep cli"')
  
@task
@roles('uat_reproc')
def copy_libs():
  put('/Users/oliver/SourceCode/scripts/crap/uat/lib/*jar','/home/crap/uat_reproc/lib/')