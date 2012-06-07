from fabric.api import *


READ_PERMISSIONS='list,search,readattr,readextattr,readsecurity'

INHERIT_PERMISSIONS='file_inherit,directory_inherit'

def check_permissions(folder):
    
    sudo('ls -le %s' % folder)
    
def clear_permissions(folder):
    
    sudo('chmod -R -E %(folder)s' % locals())
    
def read_permissions(folder,name,isGroup=False):
       
    if isGroup:
        usrStr='group:%(name)s' % locals()
    else:
        usrStr='user:%(name)s' % locals()
     
    perms=','.join([READ_PERMISSIONS,INHERIT_PERMISSIONS])
    
    sudo('chmod -R +a "%(usrStr)s allow %(perms)s" %(folder)s' % locals())
    
        
    
    
    
def test():
    
    read_permissions('/usr/local/web','www')