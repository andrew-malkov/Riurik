import os, subprocess, socket, time, random

hem = None

def spine(ctx):
	return ctx.get('spine', None) != None

def wait_hem(host, port, timeout=10):
	while True:
		time.sleep(1)
		try:
			s = socket.create_connection( (host, port), 20)
			return s.close()
		except socket.error:
			timeout = timeout -1
			if not timeout:
				raise Exception('hem server start timeout')

def run_hem_server(ctx, path, fullpath, server):
	global hem
	if hem:
		hem.terminate()
		hem = None

	port = ctx.get('port', 80)
	host = ctx.get('host', server)
	hem_path = os.path.join(fullpath, "../node_modules/hem/bin/hem")
	hem = subprocess.Popen(
		(os.path.normpath(hem_path), "server", "--port=%s" % port),
		cwd = fullpath,
		stdout = open( '/dev/null', 'w' ), stderr = subprocess.STDOUT
	)

	wait_hem( host, port )
	return "http://%s:%s/test?_=%s" % ( host, port, random.random() )
