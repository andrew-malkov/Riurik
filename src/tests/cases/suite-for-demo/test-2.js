module('demo', {
  
  teardown: function() {
    delete_folder( context.root + '/' + context.suite_name );
  }

});

asyncTest('create suite', function() {
  $.when( frame.go(context.root)).then(function() {
    _$('a#new-suite').click();
    equal(_$('#create-dir-index-dialog').is(":visible"), true, 'dialog is visible');
    equal(_$('.ui-dialog-title').text(), _$('a#new-suite').text(), 'dialog has right title');
    
    _$('#object-name').val(context.suite_name);
    _$('#create-folder-btn').click();
    $.when( frame.load() ).then(function(_$) {
      equal(_$('li#' + context.suite_name + '.folder').length, 1, 'new folder has been created');
      start();
    });
  })
});