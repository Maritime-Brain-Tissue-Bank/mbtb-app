const Browser = require('zombie');
Browser.localhost('localhost', 1337);

// This test check user login against correct and wrong credentials
describe('User Login - Successful', function() {

  const browser = new Browser();

  before(function(done) {
    browser.visit('/login', done);
  });

  describe('submits form', function() {

    before(function(done) {
      browser.fill('user_email',    'meow@gmail.com');
      browser.fill('user_password', 'wbwIHCqRjEiMTeh');
      browser.pressButton('#submit_btn', done);
    });

    it('Correct Credentials', function() {
      browser.assert.success();
      browser.assert.text('title', 'Home');
    });


  });

});


describe('User Login - Fail', function() {

  const browser = new Browser();

  before(function(done) {
    browser.visit('/logout');
    browser.visit('/login', done);
  });

  describe('submits form', function() {

    before(function(done) {
      browser.fill('user_email',    'fake@email.id');
      browser.fill('user_password', 'fake_password');
      browser.pressButton('#submit_btn', done);
    });

    it('Wrong Credentials', function() {
      browser.assert.text('#error_msg', 'Invalid username/password');
    });

  });
});

