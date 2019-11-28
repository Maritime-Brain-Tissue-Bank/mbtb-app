const Browser = require('zombie');
Browser.localhost('localhost', 1337);




// This test login in admin portal and delete test user requests
describe('Admin Delete - Registration Requests', function() {

  const browser = new Browser();

  before(function(done) {
    browser.visit('/admin_login', done);
  });

  describe('admin logged-in', function() {

    before(function(done) {
      browser.fill('admin_email',    'admin@mbtb.ca');
      browser.fill('admin_password', 'asdfghjkl123');
      browser.pressButton('#submit_btn', done);
    });

    it('Deleting requests', function(done) {
      browser.assert.text('title', 'Admin - Home');
      browser.visit('/view_new_requests', function () {
        browser.assert.text('title', 'User Requests');
        browser._setCheckbox("#select_all", true);

        browser.pressButton('#deny_request_btn');
        done();
      });
    });

  });

});
