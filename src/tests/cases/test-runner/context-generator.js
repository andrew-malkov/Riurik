module('context generator');

QUnit.setup(function() {
  context.setup_value = 10;
  context.hidden_file = '.hidden-file.js';
  context.suite_path = 'tests/suite-for-testing';
  context.hidden_path = context.suite_path + '/' + context.hidden_file;
  var path = 'actions/suite/run/?path=/' + context.suite_path + '&context=localhost';
  context.url = contexter.URL(context, path);
  
  delete_test( context.hidden_path );
  create_test( context.hidden_file, context.suite_path );
});

test('context is generated', function() {
  QUnit.log(context);
  
  ok( typeof context != 'undefined', 'context is generated' );
  ok( context.host != 'localhost', 'localhost is translated into local machine name' );
  equal( context.var1, 'value2', 'variable value corresponds to context' );
  equal( context.setup_value, 10, 'value from setup is available' );
  equal( library1.method1(20), 20, 'method from library 1 is available' );
  equal( library2.method2(40), 40, 'method from library 2 is available' );
  equal( library3.method3(60), 60, 'method from library 3 is available' );
  
});

asyncTest('hidden file is not included into suite', function() {
  $.when( frame.go( context.url ) ).then(function(_$) {

    $.each( frame.window().context.include, function(index, value){ 
      ok( value != context.hidden_file, value );
    });
    
    start();
  });
});

QUnit.teardown(function() {
  delete_test( context.hidden_path );
});