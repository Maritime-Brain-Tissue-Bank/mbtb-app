describe('admin view single user',function(){
  beforeAll(function () {
    browser.get('http://localhost:1337/view_current_users/1');
    browser.waitForAngularEnabled(false);
    element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
    element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
    element(by.id("submit_btn")).click();
  });

  it('should display single user information', function () {
    browser.get('http://localhost:1337/view_current_users/1');
    expect(browser.getTitle()).toEqual('Admin - View Current User');
    //single user table
    var table = element(by.css('.table'));
    expect(table.isDisplayed()).toBe(true);
    //test data binding
    expect(element(by.exactBinding('details.title')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.first_name')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.middle_name')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.last_name')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.email')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.institution')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.department_name')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.position_title')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.address_line_1')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.address_line_2')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.city')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.province')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.country')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.postal_code')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.comments')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.active_since')).isPresent()).toBe(true);

    //test suspend single user button
    expect(element(by.id('suspend_single_user')).getText()).toBe('Suspend');


  });

  afterAll(function () {
    element(by.id("admin_logout")).click();
  });

});
