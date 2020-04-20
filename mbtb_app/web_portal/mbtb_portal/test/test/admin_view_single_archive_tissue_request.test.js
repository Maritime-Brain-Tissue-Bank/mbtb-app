describe('admin - view single archive tissue request', function () {

  beforeAll(function () {
    browser.get('http://localhost:1337/view_single_archive_tissue_request/6');
    browser.waitForAngularEnabled(false);
    element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
    element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
    element(by.id("submit_btn")).click();
  });

  it('should have single archive tissue request table', function () {
    browser.get('http://localhost:1337/view_single_archive_tissue_request/6');
    expect(browser.getTitle()).toEqual('View Archived Tissue Request');

    var table = element(by.css('.table'));
    expect(table.isDisplayed()).toBe(true);

    expect(element.all(by.css('.table tbody tr')).count()).toEqual(18);

    expect(element.all(by.css('.table tbody tr td')).count()).toEqual(36);
    //test data binding
    expect(element(by.exactBinding('details.tissue_request_number')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.title')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.first_name')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.last_name')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.email')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.institution')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.department_name')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.city')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.province')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.postal_code')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.phone_number')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.project_title')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.source_of_funding')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.abstract')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.received_date')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.approval_date')).isPresent()).toBe(true);
    expect(element(by.exactBinding('details.reverted_date')).isPresent()).toBe(true);

    //should be revert and delete button
    expect(element(by.id('edit_btn')).getText()).toBe('Revert');
    expect(element(by.id('delete_btn')).getText()).toBe('Delete');


  });

  afterAll(function () {
    element(by.id("admin_logout")).click();

  });
});

