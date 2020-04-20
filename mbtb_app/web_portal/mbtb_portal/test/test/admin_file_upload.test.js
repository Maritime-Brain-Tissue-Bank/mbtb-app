describe('Admin file upload', function () {

  beforeAll(function () {
    browser.get('http://localhost:1337/file_upload');
    browser.waitForAngularEnabled(false);
    element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
    element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
    element(by.id("submit_btn")).click();
  });

  //test admin upload file
  it('it should upload file and view guide', function () {
    browser.get('http://localhost:1337/file_upload');
    expect(browser.getTitle()).toEqual('Admin - Upload File - Add New Data');

    //test data guide link
    expect(element(by.linkText('guide')).getAttribute('href')).toEqual('http://localhost:1337/data_uploading_guide');

    //replace csv file in the test repo
    //update fileToUpload and path
    //test upload file
    var path = require('path');
    var fileToUpload = '../test_file.csv';
    var absolutePath = path.resolve('../test',fileToUpload);

    element(by.css('input[type="file"]')).sendKeys(absolutePath);
    expect(element(by.css('input[type="file"]')).getAttribute('value')).toBe('C:\\fakepath\\test_file.csv');
    element(by.css('button[type="submit"]')).click().then(function () {
      console.log('button clicked');
    });


  });

  afterAll(function () {
    element(by.id("admin_logout")).click();
  });


});
