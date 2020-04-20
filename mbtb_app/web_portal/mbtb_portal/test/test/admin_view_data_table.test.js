describe('Admin view data test', function () {

  beforeAll(function () {
    /*browser.get('http://localhost:1337/admin_view_data');*/
    browser.get('https://mbtb-portal.herokuapp.com/admin_view_data');
    browser.waitForAngularEnabled(false);
    element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
    element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
    element(by.id("submit_btn")).click();
  });
  //test admin - view data
  it('admin - view data table', function () {

    // browser.get('http://localhost:1337/admin_view_data');
    browser.get('https://mbtb-portal.herokuapp.com/admin_view_data');
    expect(browser.getTitle()).toEqual('Admin - View Data');
    element(by.id("search_btn")).click();
    var table = element(by.css('.table'));
    expect(table.isDisplayed()).toBe(true);
    //count rows
    //update rows when having more data
    expect(element.all(by.css(".table tbody tr")).count()).toEqual(10);

    //count columns
    expect(element.all(by.css(".table thead tr th")).count()).toEqual(11);

    //test table header
    var headers = element.all(by.css('.table thead tr th')).map(function (elm) {
      return elm.getText();
    });
    expect(headers).toEqual([
      "No",
      "MBTB Code",
      "Sex",
      "Age",
      "Postmortem Interval",
      "Time in Fix (Days)",
      "Preservation Method",
      "Clinical Diagnosis",
      "Neuropathological Diagnosis",
      "Tissue Type",
      "Storage Year"
    ]);


    //get rows
    var rows = table.all(by.tagName("tr"));
    //get cells
    var cells = rows.all(by.tagName("td"));
    //test cell MBTB code BB00-008
    expect(cells.get(1).getText()).toEqual("BB00-001");


    //download all
    element(by.css('[ng-click="download_csv_file(\'all\')"]')).click();
    //filepath
    var filename='/Users/yichaoliang/Downloads/MBTB_Data.csv';
    var fs= require('fs');
    //download filter
    //select parameter
    /* element(by.css('[ng-click="download_csv_file(\'filtered\')"]')).click();*/

    browser.driver.wait(function () {
      return fs.existsSync(filename);
    },30000).then(function () {
      expect(fs.readFileSync(filename, { encoding: 'utf8' })).toContain("MBTB Data");
    });

  });

  afterAll(function () {
    element(by.id("admin_logout")).click();
  });

});
