describe('admin view new tissue request', function () {
  beforeAll(function () {
    browser.get('http://localhost:1337/get_new_tissue_requests');
    browser.waitForAngularEnabled(false);
    element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
    element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
    element(by.id("submit_btn")).click();
  });

  //test tissue request archive table
  it('should be a table displaying new tissue request and approve/delete button', function () {
    browser.get('http://localhost:1337/get_new_tissue_requests');
    expect(browser.getTitle()).toEqual('Admin - Tissue Requests');
    var table = element(by.css('.table'));
    expect(table.isDisplayed()).toBe(true);

    expect(element.all(by.css(".table thead tr th")).count()).toEqual(17);

    var headers = element.all(by.css('.table thead tr th')).map(function (elm) {
      return elm.getText();
    });
    expect(headers).toEqual([
      "",
      "Title",
      "First Name",
      "Last Name",
      "Email",
      "Institution",
      "Department",
      "City",
      "Province",
      "Postal/Zip Code",
      "Phone",
      "Fax",
      "Project Title",
      "Source of Funding",
      "Abstract",
      "Received Date",
      "Tissue Request No"
    ]);

    //test approve/delete buttons
    expect(element(by.id('accept_tissue_request_btn')).getText()).toBe('Approve');
    expect(element(by.id('delete_tissue_request_btn')).getText()).toBe('Delete');

  });
});

