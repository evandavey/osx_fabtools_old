from fabric.api import *
from fabric.colors import *
import launchctl
from fabric.contrib.files import exists

dst='/Applications/calibre.app'
label='org.calibre.server'
url='http://status.calibre-ebook.com/dist/osx32'

def installed():
    
    with settings(hide('everything')):
        if exists(dst):
            return True
        else:
            return False

def uninstall():
    
    if installed():
        launchctl.delete(label)
        sudo('rm -rf %s' % dst)
        

def install_launchdaemon(library_path):
    
    args=[
        '/Applications/calibre.app/Contents/MacOS/calibre-server',
        '--port=8081',
        '--with-library=%(library_path)s' % locals(),
    
    ]
    
    launchctl.install2(label,args)

def install():
    
    
    uninstall() #remove old
     
    utils.download_and_mount('calibre',url)
    
    #move to Applications
    sudo('cp -r /Volumes/calibre/calibre.app /Applications/')
    
    
    
    
    launchctl.install(label,'')
    
def status():
    
    if not installed():
        return blue('not installed')

    with settings(hide('everything')):
        pid=launchctl.pid(label)
    
    if pid:
        pid=int(pid)
        return green('running (id=%d)' % pid)
    else:
        return red('not running')
