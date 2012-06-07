"""
Launchctl fabric commands
"""

from fabric.api import *
from fabric.colors import *

def install(label,src,dst):
    
    with settings(warn_only=True):
        plist_src='%s/launchdaemons/%s.plist' % (src,label)
        plist_dst='%s/%s.plist' % (dst,label)
        unload(label)
        put(plist_src,plist_dst)
        sudo('mv %s %s' % (plist_dst,'/Library/LaunchDaemons/'))
        sudo('chown root:admin %s' % ('/Library/LaunchDaemons/%s.plist' % label))
        load(label)
        cmd('start',label)
    
def load(label):
    sudo('launchctl load %s/%s.plist' % ('/Library/LaunchDaemons/',label))
    
def unload(label):
    sudo('launchctl unload %s/%s.plist' % ('/Library/LaunchDaemons/',label))

def delete(label):
    unload(label)
    sudo('rm -f %s' % ('/Library/LaunchDaemons/%s.plist' % label))

def cmd(cmd,label):
    
    with settings(warn_only=True):
        print(red('Launchctl: %s %s' % (cmd,label)))
        sudo('launchctl %s %s' % (cmd,label))
        
def pid(label):
    
    with hide('everything','debug'):
        pid=sudo("""launchctl list|grep %s|awk '{ printf $1" "}'""" % label)
    return pid