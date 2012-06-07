from fabric.api import *
from fabric.colors import *

def isRVMInstalled():
    
    with settings(hide('running', 'stdout', 'warnings')):
        return int(run('rvm 2>&1 1>/dev/null | wc -l')) == 0
    
    
def status():
    
    if not isRVMInstalled():
         return red('rvm not installed')
    else:
        return green('rvm installed')


def uninstall_rvm():
    
    sudo('rm -rf /usr/local/rvm')

def install_rvm():
    
    #performs a multi-user install in /usr/local/rvm 
    #see https://rvm.io/rvm/install/
    uninstall_rvm()
    sudo('curl -L get.rvm.io | sudo bash -s stable')

def install_ruby(version):
    
    run('rvm install %(version)s' % locals())
    
def install_ree():
    
    install_ruby('ree')
    
def bootstrap():
    """
    Installs custom ruby settings
    """
    
    install_rvm()
    users.add_to_group('cochranedavey','rvm')
    users.add_to_group('www','rvm')
    install_ruby('1.9.2') 
    
    


