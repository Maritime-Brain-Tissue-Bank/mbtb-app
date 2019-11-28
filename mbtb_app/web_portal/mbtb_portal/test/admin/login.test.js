const Browser = require('zombie');
Browser.localhost('localhost', 1337);

// This test check Admin login against correct and wrong credentials
describe('Admin Login - Successful', function() {

  const browser = new Browser();

  before(function(done) {
    browser.visit('/admin_login', done);
  });

  describe('submits form', function() {

    before(function(done) {
      browser.fill('admin_email',    'admin@mbtb.ca');
      browser.fill('admin_password', 'asdfghjkl123');
      browser.pressButton('#submit_btn', done);
    });

    it('Correct Credentials', function() {
      browser.assert.success();
      browser.assert.text('title', 'Admin - Home');
    });


  });

});

describe('Admin Login - Fail', function() {

  const browser = new Browser();

  before(function(done) {
    browser.visit('/admin_logout');
    browser.visit('/admin_login', done);
  });

  describe('submits form', function() {

    before(function(done) {
      browser.fill('admin_email',    'fake@email.id');
      browser.fill('admin_password', 'fake_password');
      browser.pressButton('#submit_btn', done);
    });

    it('Wrong Credentials', function() {
      browser.assert.text('#error_msg', 'Invalid username/password');
    });

  });
});

