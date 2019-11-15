const Browser = require('zombie');
Browser.localhost('localhost', 1337);

// This test check user login against correct and wrong credentials
describe('User Registration - Successful', function() {

  const browser = new Browser();

  before(function(done) {
    browser.visit('/register', done);
  });

  describe('submits form', function() {

    before(function(done) {
      browser.fill('first_name',    'test');
      browser.fill('last_name', 'sails js');
      browser.fill('email',    'sailsjs_test@gmail.com');
      browser.fill('institution', 'test');
      browser.fill('department_name',    'test');
      browser.fill('current_position', 'test');
      browser.fill('city',    'test');
      browser.fill('province', 'test');
      browser.fill('country',    'test');
      browser.fill('comments', 'test');
      browser._setCheckbox("agree_terms_checkbox", true);
      browser.pressButton('#submit_btn', done);
    });

    it('Correct Registration Data', function() {
      browser.assert.success();
      browser.assert.text('#message_title', 'Confirmation');
    });


  });

});


describe('User Registration - Error', function() {

  const browser = new Browser();

  before(function(done) {
    browser.visit('/register', done);
  });

  describe('submits form', function() {

    before(function(done) {
      browser.fill('first_name',    'test');
      browser.fill('last_name', 'sails js');
      browser.fill('email',    'sailsjs_test@gmail.com');
      browser.fill('institution', 'test');
      browser.fill('department_name',    'test');
      browser.fill('current_position', 'test');
      browser.fill('city',    'test');
      browser.fill('province', 'test');
      browser.fill('country',    'test');
      browser.fill('comments', 'test');
      browser._setCheckbox("agree_terms_checkbox", true);
      browser.pressButton('#submit_btn', done);
    });

    it('User Registration with Same Email ID', function() {
      browser.assert.text('#message_title', 'Error');
    });

  });
});

