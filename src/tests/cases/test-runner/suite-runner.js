module('suite runner', {
  setup: function() {
    var path = 'actions/suite/run/?path=/tests/suite-for-testing&context=localhost';
    context.url = contexter.URL(context, path);
  }
});

asyncTest('suite is executed', function() {
  $.when( frame.go( context.url ) ).then(function(_$) {
    
    ok( typeof frame.window().context != 'undefined', 'context is generated' );
    frame.window().QUnit.done = function(module) {
      ok( _$('#qunit-testresult').length == 1, 'test result is present');
      equal( _$('.test-name').length, 5, 'all tests are ran' );

      start();
    }
  });
});