"""
Launchctl fabric commands
"""

from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import exists,upload_template
import os

def install2(label,args,dst='/Library/LaunchDaemons'):
    """
    Creates and installs a launchdaemon with the specified args array
    """
    
    runAtLoad=True
    keepAlive=True
    
    dst_file=os.path.join(dst,label+'.plist')
    with settings(warn_only=True):
        unload(label)
        upload_template('launchdaemon.plist', dst_file, backup = False, context=locals(), use_jinja=True, use_sudo=True, template_dir='templates')
        sudo('chown root:admin %s' % (dst_file))
        
        load(label)
        cmd('start',label)

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
    
def unload(label, dst='/Library/LaunchDaemons'):
    
    dst_file=os.path.join(dst,label+'.plist')
    if exists(dst_file):
        sudo('launchctl unload %(dst_file)s' % locals())

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