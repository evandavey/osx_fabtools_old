from fabric.api import *
from fabric.colors import *

def isBaseInstalled():
    
    with settings(hide('running', 'stdout', 'warnings')):
        return int(run('brew 2>&1 1>/dev/null | wc -l')) == 0

def base_install():
    
    run('/usr/bin/ruby -e "$(/usr/bin/curl -fksSL https://raw.github.com/mxcl/homebrew/master/Library/Contributions/install_homebrew.rb)"')
    
def install_packages():
    
    pkgs=" ".join(env.homebrew_packages)
    run('brew install %s' % (pkgs))


def installed(pkg):
    
    pkgs=installed_pkgs()

    if pkg in pkgs:
        return True
    else:
        return False

def install(pkg):
    run('brew install %s' % (pkg))
    

def installed_pkgs():
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        installed=run('brew list').strip()
        return installed.split()
 
 
def status():
    
    
    if not isBaseInstalled():
        return red('not installed')
    else:
        pkgs=', '.join(installed_pkgs())
        return green('installed') + '\n%s\n' % pkgs