describe('admin archive tissue request', function () {
  beforeAll(function () {
    browser.get('http://localhost:1337/get_archive_tissue_requests');
    browser.waitForAngularEnabled(false);
    element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
    element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
    element(by.id("submit_btn")).click();
  });

  //test tissue request archive table
  it('should be archive tissue request table and revert/delete button', function () {
    browser.get('http://localhost:1337/get_archive_tissue_requests');
    expect(browser.getTitle()).toEqual('Admin - Archived Tissue Requests');
    var table = element(by.css('.table'));
    expect(table.isDisplayed()).toBe(true);

    expect(element.all(by.css(".table thead tr th")).count()).toEqual(18);

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
      "Approval Date",
      "Tissue Request No"
    ]);

    //revert/delete button
    expect(element(by.id('revert_tissue_request_btn')).getText()).toBe('Revert');
    expect(element(by.id('delete_archive_tissue_request_btn')).getText()).toBe('Delete');


  });
});

