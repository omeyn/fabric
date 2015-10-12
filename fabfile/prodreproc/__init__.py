from fabric.api import *

@task
@parallel
@roles('prod_reproc')
def stop():
  sudo('sh -c "cd /home/crap/prod_reproc/bin && /home/crap/prod_reproc/bin/stop-processors.sh"')
  
@task
@parallel
@roles('prod_reproc')
def start_verbatim():
  sudo('sh -c "cd /home/crap/prod_reproc/bin && /home/crap/prod_reproc/bin/start-processor-verbatim.sh"')

@task
@parallel
@roles('prod_reproc')
def start_interp():
  sudo('sh -c "cd /home/crap/prod_reproc/bin && /home/crap/prod_reproc/bin/start-processor-interpreted.sh"')
  
@task
@parallel
@roles('prod_reproc')
def setup_dirs():
  sudo('sh -c "chown -R crap.crap /home/crap/prod_reproc"')

@task
@parallel
@roles('prod_reproc')
def check_ps():
  sudo('sh -c "ps aux | grep jav | grep cli"')