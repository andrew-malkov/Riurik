/* this test require one more riurik instance on the 8001 port
*  that will allow to test of saving test content in the editor
*  to remote file system where test will be loaded
*/
module('run test remote');

// setup creates new empty test file on a file system
QUnit.setup(function() {
  context.test_name = 'second-example.js';
  context.suite_path = 'tests/remote-tests';
  context.test_path = context.suite_path + '/' + context.test_name;
  context.test_context = 'save-remote';
  context.test_content = "test('test in iframe', function(){ok(true, 'is run')});";
  context.start = getLogs('last');
    
  var path = 'actions/test/run/?path=' + context.test_path + '&context=' + context.test_context;
  context.url = contexter.URL(context, path + "&content=" + escape(context.test_content));
    
  delete_test( context.test_path );
  create_test( context.test_name, context.suite_path );
  start();
});

asyncTest('test is run', function() {
  $('#frame').attr('src', context.url);
  $('#frame').unbind('load');
  $('#frame').load(function() {
    var logs = getLogs(context.start);
    var regex = new RegExp("Run test " + delVirtualDir(context.test_path));
    ok(regex.test(logs), regex);
    start();
  });
});

QUnit.teardown(function() {
  delete_test( context.test_path );
  start();
});