from fabric.api import *

def exists(name,group=False):
    """
    Check if user exists
    """
    
    checktype='Users'
    if group:
        checktype='Groups'
        
    
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        return int(sudo('dscl . -read /%(checktype)s/%(name)s 2>&1 1>/dev/null | wc -l' % locals())) == 0
    
def isMember(name,group):
    """
    Checks if a name is a member of group
    See http://superuser.com/questions/279891/list-all-members-of-a-group-mac-os-x
    """
    
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        return int(sudo('dsmemberutil checkmembership -U "%(name)s" -G "%(group)s" | grep "is not a member" | cut -d " " -f 1 | wc -l' % locals()))==1
        
def next_userid():
    """
    Get the next available user id
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        maxid=int(sudo("dscl . -list /Users UniqueID | awk '{print $2}' | sort -ug | tail -1"))
        return maxid+1

def next_groupid():
    """
    Get the next available group id
    """
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        maxid=int(sudo("dscl . -list /Groups PrimaryGroupID | awk '{print $2}' | sort -ug | tail -1"))
        return maxid+1
   
def create_group(name, realname, gid=None):
    """
    Creates a new group
    If group name begins with "_" (ie: it is a system group) then an alias is created
    If no gid is specified, the next available id will be used
    """

    system=False

    if name[0] == "_":
        system=True
       
    if gid is None:
        gid=next_groupid()
    
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        sudo('dscl . -create /Groups/%(name)s' % locals())
        sudo('dscl . -create /Groups/%(name)s PrimaryGroupID %(gid)s' % locals())
        sudo('dscl . -create /Groups/%(name)s RealName %(realname)s' % locals())
        sudo('dscl . -create /Groups/%(name)s Password \*' % locals())
        
        if system:
            alias=name[1:]
            sudo('dscl . -create /Groups/%(name)s RecordName %(alias)s' % locals())
    
    return gid

def show(name,group=False):
    
    checktype='Users'
    if group:
        checktype='Groups'


    with settings(hide('running')):
        sudo('dscl . -read /%(checktype)s/%(name)s' % locals())
     
def create(name, realname, home=None, shell=None, uid=None, gid=None):
    """
    Creates a new user
    If name begins with "_" (ie: it is a system group) then an alias is created
    If no gid is specified, the next available id will be used
    """

    system=False

    if name[0] == "_":
        system=True
        
    if home is None:
        home='/var/empty'
        
    if shell is None:
        shell='/usr/bin/false'
        
    if uid is None:
        uid=next_userid()
        
    if gid is None:
        return -1 #not sure what to do here
    
    with settings(hide('running', 'stdout', 'warnings'), warn_only=True):
        sudo('dscl . -create /Users/%(name)s' % locals())
        sudo('dscl . -create /Users/%(name)s UniqueID %(uid)s' % locals())
        sudo('dscl . -create /Users/%(name)s UserShell %(shell)s' % locals())
        sudo('dscl . -create /Users/%(name)s NFSHomeDirectory %(home)s' % locals())
        
        sudo('dscl . -create /Users/%(name)s PrimaryGroupID %(gid)s' % locals())
        sudo('dscl . -create /Users/%(name)s RealName %(realname)s' % locals())
        
        
        sudo('dscl . -create /Users/%(name)s Password \*' % locals()) #what about non system accounts?
        
        if system:
            alias=name[1:]
            sudo('dscl . -append /Users/%(name)s RecordName %(alias)s' % locals())
    
    return uid

def add_to_group(name,group):
    """
    Adds name to group
    http://superuser.com/questions/214004/how-to-add-user-to-a-group-from-mac-os-x-command-line
    
    """
    
    sudo('dseditgroup -o edit -a %(name)s -t user %(group)s' % locals())
    