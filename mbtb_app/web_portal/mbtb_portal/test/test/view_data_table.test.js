describe('User view data test', function () {
  beforeAll(function () {
    /*browser.get('http://localhost:1337/view_data');*/
    browser.get('https://mbtb-portal.herokuapp.com/view_data');
    browser.waitForAngularEnabled(false);
    /* element(by.css("input[name='user_email']")).sendKeys('yc441486@dal.ca');
     element(by.css("input[name='user_password']")).sendKeys('UX8Ktap36lHCpFt');*/
    element(by.css("input[name='user_email']")).sendKeys('meow@gmail.com');
    element(by.css("input[name='user_password']")).sendKeys('iBjJqBTIBBSD53p');
    element(by.id("submit_btn")).click();
  });
  //test admin - view data
  it('admin - view data table', function () {
    /* browser.get('http://localhost:1337/view_data');*/
    browser.get('https://mbtb-portal.herokuapp.com/view_data');
    expect(browser.getTitle()).toEqual('View Data');
    element(by.id("search_btn")).click();
    var table = element(by.css('.table'));
    expect(table.isDisplayed()).toBe(true);
    //count rows
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
     //test cell MBTB code BB00-001
     expect(cells.get(1).getText()).toEqual("BB00-001");

    //download all
    element(by.css('[ng-click="download_csv_file(\'all\')"]')).click();
    //download filtered data
    //select parameter
    /*element(by.css('[ng-click="download_csv_file(\'filtered\')"]')).click();*/

    //file path
    //download all data
    var filename='/Users/yichaoliang/Downloads/MBTB_Data.csv';
    //download filtered data
    /*var filename='/Users/yichaoliang/Downloads/Filtered_MBTB_data.csv';*/
    var fs= require('fs');


    browser.driver.wait(function () {
      return fs.existsSync(filename);
    },30000).then(function () {
      expect(fs.readFileSync(filename, { encoding: 'utf8' })).toContain("MBTB Data");
      //toContain("MBTB Data") if download all
      //toContain("Filtered MBTB data") if filtered
    });



  });

  afterAll(function () {
    element(by.id("user_logout")).click();
  });


});
