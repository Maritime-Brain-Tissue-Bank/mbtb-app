describe('User view data test', function () {
    beforeAll(function () {
        browser.get('http://localhost:1337/view_data');
        browser.waitForAngularEnabled(false);
        element(by.css("input[name='user_email']")).sendKeys('yc441486@dal.ca');
        element(by.css("input[name='user_password']")).sendKeys('UX8Ktap36lHCpFt');
        element(by.id("submit_btn")).click();
    });
    //test admin - view data
    it('admin - view data table', function () {
        browser.get('http://localhost:1337/view_data');
        expect(browser.getTitle()).toEqual('View Data');
        element(by.id("search_btn")).click();
        var table=element(by.css('.table'));
        expect(table.isDisplayed()).toBe(true);
        //count rows
        expect(element.all(by.css(".table tbody tr")).count()).toEqual(10);
        //test table header
        var headers=element.all(by.css('.table thead tr th')).map(function(elm){
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
        var rows=table.all(by.tagName("tr"));
        //get cells
        var cells = rows.all(by.tagName("td"));
        //test cell MBTB code BB00-001
        expect(cells.get(1).getText()).toEqual("BB00-001");
    });

    afterAll(function(){
        element(by.id("user_logout")).click();
    });




});
