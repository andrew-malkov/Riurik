import os, re, simplejson
from logger import log
import settings, config, contrib
from django.template import Context, Template
import socket
		
def host(instance, resolve=True):
	key = 'host'
	if resolve:
		return contrib.resolveRemoteAddr(instance.get(key))
	return instance.get(key)
		
def get(name, section='default'):
	return context(name, section)

def get_URL(instance, resolve=False):
	url = instance.get('url')
	if not url:
		host = instance.get('host')
		if host == 'localhost':
			host = socket.gethostname()
		if resolve:
			host = contrib.resolveRemoteAddr(host)
		url =  'http://%s:%s' % (host, instance.get('port'))
	return url

def render(ctx):
	vars = patch(ctx)
	t = Template("""{% load json_tags %}
		var context = {
			{% for option in options %}
				{{ option.0 }}: {{ option.1|json }}{% if not forloop.last %},{% endif %}
			{% endfor %}
		};
	""")
	c = Context();
	c['options'] = []
	for name, value in vars:
		c['options'] += [ (name, value,), ]
	return t.render(c)

def patch(ctx):
	vars = ctx.items()
	hasInclude = False
	hasExclude = False
	localhost = False
	for i,v in vars:
		if i == 'include':
			hasInclude = True
		
		if i == 'exclude':
			hasExclude = True
			
		if i == 'host' and v == 'localhost':
			localhost = True
			
	if not hasInclude:
		exclude = []
		if hasExclude:
			exclude = simplejson.loads(ctx.get( option='exclude' ))
		include = []
		for root, dirs, files in os.walk(ctx.get_folder()):
			for file in files:
				if re.match('^.*\.js$', file):
					if file in exclude:
						continue
					file_abspath = os.path.abspath(os.path.join(root, file))
					file_relpath = file_abspath.replace(os.path.abspath(ctx.get_folder()), '').lstrip('/').lstrip('\\')
					include += [ str(file_relpath) ]
		vars = tuple(list(vars) + [ ('include', str(include).replace('\'','\"')) ])
		
	if localhost:
		vars = list(vars)
		vars.remove(('host', 'localhost'))
		vars = tuple( vars + [ ('host', socket.gethostname()) ] )

	return vars

class context():
	
	def __init__(self, test, section='default'):
		test = os.path.join(settings.STATIC_TESTS_ROOT, test)
		if os.path.isdir(test):
			self.inifile = os.path.join(test, settings.TEST_CONTEXT_FILE_NAME)
		else:
			self.inifile = os.path.join(os.path.dirname(test), settings.TEST_CONTEXT_FILE_NAME)
		self.section = section
		log.debug('context: %s, section: %s, test: %s' % (self.inifile, self.section, test))
		
	def get(self, option):
		value = config.get(self.inifile, self.section, option)
		log.debug('get context option: %s=%s' % (option, value))
		return value
	
	def set(self, option, value):
		config.set(self.inifile, self.section, option, value)
		log.debug('set context option: %s=%s' % (option, value))

	def items(self):
		log.debug('context get items(): %s, section: %s' % (self.inifile, self.section))
		return config.items(self.inifile, self.section)
	
	def sections(self):
		return config.sections(self.inifile)
	
	def get_folder(self):
		return os.path.dirname(self.inifile)
