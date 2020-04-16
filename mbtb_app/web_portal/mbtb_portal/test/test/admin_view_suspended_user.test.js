describe('Admin view suspended user', function () {

  beforeAll(function () {
    browser.get('http://localhost:1337/view_suspended_users');
    browser.waitForAngularEnabled(false);
    element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
    element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
    element(by.id("submit_btn")).click();
  });

  //test admin upload file
  it('admin - view suspended user', function () {
    browser.get('http://localhost:1337/view_suspended_users');
    expect(browser.getTitle()).toEqual('Admin - Suspended Users');

    var table = element(by.css('.table'));
    expect(table.isDisplayed()).toBe(true);

    //test table header
    var headers = element.all(by.css('.table thead tr th')).map(function (elm) {
      return elm.getText();
    });
    expect(headers).toEqual([
      "",
      "Title",
      "First Name",
      "Middle Name",
      "Last Name",
      "Email",
      "Institution",
      "Department",
      "Position",
      "Address Line 1",
      "Address Line 2",
      "City",
      "Province",
      "Country",
      "Postal/Zip Code",
      "Comments",
      "Active Since"
    ]);

    //test revert button
    expect(element(by.id('revert_suspended_user_btn')).getText()).toBe('Revert');


  });

  afterAll(function () {
    element(by.id("admin_logout")).click();
  });


});
