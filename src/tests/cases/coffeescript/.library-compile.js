// Generated by CoffeeScript 1.2.1-pre

module('coffee-script');

test('including compiled global coffee library', function() {
  ok(typeof global_coffee_lib !== "undefined" && global_coffee_lib !== null, 'global lib compiled and global_coffee_lib is exists');
  return ok(global_coffee_lib(), 'global_coffee_lib is executable');
});

test('including compiled local coffee library', function() {
  ok(typeof local_coffee_lib !== "undefined" && local_coffee_lib !== null, 'local lib compiled and local_coffee_lib is exists');
  return ok(local_coffee_lib(), 'local_coffee_lib is executable');
});
