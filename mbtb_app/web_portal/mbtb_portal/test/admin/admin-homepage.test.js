const Browser = require('zombie');
var sails = require('sails');

Browser.localhost('localhost', 1337);
const browser = new Browser();

it('Admin Homepage loaded', function() {
  browser.visit('/admin', function (err) {
    if (err) throw err;
    browser.assert.text('title', 'Admin - Home')
  });
});



