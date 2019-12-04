describe('View Detail Test',function(){
    beforeAll(function(){
        browser.get('http://localhost:1337/admin_view_data/1');
        browser.waitForAngularEnabled(false);
        element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
        element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
        element(by.id("submit_btn")).click();
    });

    it('view record 1',function(){
        browser.get('http://localhost:1337/admin_view_data/1');
        expect(browser.getTitle()).toEqual('View Record');
        //get table
        var table=element(by.css('.table'));
        expect(table.isDisplayed()).toBe(true);
        //rows count
        expect(element.all(by.css(".table tbody tr")).count()).toEqual(21);
        //test header
        var headers=element.all(by.css('.table thead tr th')).map(function(elm){
            return elm.getText();
        });
        expect(headers).toEqual([
            "Parameter",
            "Detail"
        ]);
        //get rows
        var rows=table.all(by.tagName("tr"));
        //get cell
        var cells = rows.all(by.tagName("td"));

        //test data in table: MBTB code BB00-001
        expect(cells.get(1).getText()).toEqual("BB00-001");
    });
    //log out after all
    afterAll(function(){
        element(by.id("logout")).click();
    });

});


