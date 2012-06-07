from fabric.api import *


def install_easy_install():
    pass
    
def install_pip():
    pass
    
def install_virtualenv():
    pass

def pip(args,sudo=False):
    
    if sudo:
        sudo('pip %(args)s' % args)
    else:
        run('pip %(args)s' % args)
    
    
def mkvirtualenv():
    pass
    
    

#virtual env wrapper


    
