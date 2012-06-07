# OSX Fabtools

Set of fabric scripts for use on an OSX personal server

* gitserver.py - tools for installing git, git web daemon and gitlabhq

* homebrew.py - tools for using the Homebrew package manager

* launchtl.py - tools for managing daemons

* permissions.py - tools for managing permissions

* ruby.py - tools for installing and using RVM

* users.py - user management tools

* utils.py - misc tools

* web.py - tools for setting up a web server

* wordpress.py - tools for setting up wordpress

* redmine.py - tools for setting up a redmine project management server

* django.py - tools for setting up a django deployments

## Status

Currently a WIP.  Collaboration welcome and encouraged.

## Dependencies

* Jinja2

## Usage

Import the tools into a master fabfile and call functions as necessary.  The status function of each module can be used to quickly display server status.  For example

	def status():
    
	cmds=[
		{'name':'homebrew','status':homebrew.status()},
		{'name':'ruby','status':ruby.status()},
		]

	with settings(hide('running')):
		print(blue('Server Status'))
		print 'Uptime: ' + utils.uptime()
		for c in cmds:
			print(c['name'] + " - " + c['status'])




