describe('Admin view current users', function () {

  beforeAll(function () {
    browser.get('http://localhost:1337/view_current_users');
    browser.waitForAngularEnabled(false);
    element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
    element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
    element(by.id("submit_btn")).click();
  });

  //test admin upload file
  it('admin - view current users', function () {
    browser.get('http://localhost:1337/view_current_users');
    expect(browser.getTitle()).toEqual('Admin - Current Users');

    var table = element(by.css('.table'));
    expect(table.isDisplayed()).toBe(true);

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

    //test suspend user button
    expect(element(by.id('suspend_user_btn')).getText()).toBe('Suspend');


  });

  afterAll(function () {
    element(by.id("admin_logout")).click();
  });


});
