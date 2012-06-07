from fabric.api import *

def uptime():
    with settings(hide('running','stdout')):
        return run('uptime')

def download_and_mount(name,url):
    
    dmgfile="%(name)s.dmg" % locals()
    
    run('wget -O %(dmgfile)s %(url)s' % locals())
    
    #mount image
    run('hdiutil attach -mountpoint /Volumes/%(name)s %(name)s.dmg' % locals())



# todo: migrate to Fabric template system
def open_file_and_replace(src,dest,replace_dict):
	""" replaces <key> in src with val from key,val of replace_dict with supplied values and saves as dest 
	"""

	f=open(src,'r')
	o=open(dest,'w')

	for line in f.readlines():
		for k,r in replace_dict.iteritems():
			line=line.replace('<%s>' % k,'%s' % r)

		o.write(line)

	f.close()
	o.close()