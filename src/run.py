import os
from django.http import Http404, HttpResponse, HttpResponseRedirect
from error import handler as error_handler
from serving import add_request_handler
import context, settings, contrib
import coffeescript, cucumber
import dir_index_tools
from logger import log
from plugins.spine import spine

@add_request_handler
@error_handler
def test(request, RequestHandler):
	fullpath = RequestHandler.get_full_path()
	path = contrib.normpath(request.REQUEST["path"])
	context_name = request.REQUEST.get("context", None)
	ctx = context.get(RequestHandler, section=context_name)

	log.info('run test %s with context %s' % (path, context_name))
	server = request.get_host()
	contextjs = context.render(RequestHandler, ctx, server, context_name)
	log.debug('contextJS: '+ contextjs)

	target = contrib.get_runner_url(ctx, server)
	log.info('target of test %s is %s' % (path, target))

	dir_index_tools.savetest(request.REQUEST.get('content', None), fullpath)
	test_content = request.REQUEST.get("content", open(fullpath, 'r').read())
	
	saveLocalContext(fullpath, contextjs)
	if coffee(path):
		path = coffeescript.compile2js(test_content, path, fullpath)

	engine = 'qunit'
	if cucumber.cucumber(path, ctx):
		engine = 'cucumber'
		if path.endswith(settings.CUCUMBER_FILE_EXT):
			path = cucumber.compile2js(path, fullpath)

	testLoaderUrl = ctx.get('test_loader_url', settings.EXEC_TESTS_CMD)
	url = "http://%s/%s?server=%s&engine=%s&path=/%s" % (target, testLoaderUrl, server, engine, path)
	log.info("redirect to run test %s" % url)
	return HttpResponseRedirect(url)

@add_request_handler
@error_handler
def suite(request, RequestHandler):
	fullpath = RequestHandler.get_full_path()
	path = contrib.normpath(request.REQUEST["path"])
	context_name = request.REQUEST["context"]
	ctx = context.get(RequestHandler, section=context_name)

	log.info('run suite %s with context %s' % (path, context_name))
	server = request.get_host();
	if spine.spine(ctx):
		url = spine.run_hem_server(ctx, path, fullpath, server)
	else:
		compileSuiteCoffee(path, fullpath)
		contextjs = context.render(RequestHandler, ctx, server, context_name)

		target = contrib.get_runner_url(ctx, server)
		log.info('target of suite %s is %s' % (path, target))

		saveLocalContext(fullpath, contextjs)

		engine = 'qunit'
		if cucumber.cucumber(path, ctx):
			engine = 'cucumber'
			compileSuiteCucumber(path, fullpath)

	
		testLoaderUrl = ctx.get('test_loader_url', settings.EXEC_TESTS_CMD)
		url = "http://%s/%s?server=%s&engine=%s&path=/%s" % ( target, testLoaderUrl, server, engine, path )

	log.info("redirect to run suite %s" % url)
	return HttpResponseRedirect( url )

def compileSuiteCucumber(path, suite_path):
	features = contrib.enum_files_in_folders(
			suite_path,
			lambda file_: not file_.endswith(settings.CUCUMBER_FILE_EXT)
	)
	for feature in features:
		fullpath = testFullPath(suite_path, feature)
		log.debug('compile %s' % fullpath)
		cucumber.compile2js(path, fullpath)

def compileSuiteCoffee(path, suite_path):
	contrib.cleandir(suite_path, '.*.js')
	tests = contrib.enum_files_in_folders(
			suite_path,
			lambda file_: not file_.endswith(settings.COFFEE_FILE_EXT)
	)
	for test in tests:
		fullpath = testFullPath(suite_path, test)
		coffeescript.compile2js(None, None, fullpath)

def testFullPath(suite_path, test):
	return os.path.join(suite_path, test)

def coffee(path):
	return path.endswith('.coffee')

def saveLocalContext(fullpath, contextjs):
	if os.path.isdir(fullpath):
		contextjs_path = os.path.join(fullpath, settings.TEST_CONTEXT_JS_FILE_NAME)
	else:
		contextjs_path = os.path.join(os.path.dirname(fullpath), settings.TEST_CONTEXT_JS_FILE_NAME)
	f = open(contextjs_path, 'wt')
	f.write(contextjs)
	f.close()