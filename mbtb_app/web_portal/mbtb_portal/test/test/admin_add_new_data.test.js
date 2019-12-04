describe('Admin dd new data test', function() {

    beforeAll(function(){
        browser.get('http://localhost:1337/add_new_data');
        browser.waitForAngularEnabled(false);
        element(by.css("input[name='admin_email']")).sendKeys('admin@mbtb.ca');
        element(by.css("input[name='admin_password']")).sendKeys('asdfghjkl123');
        element(by.id("submit_btn")).click();
    });

    //test admin - add new data
     it('admin- add new data test',function(){
         browser.get('http://localhost:1337/add_new_data');
         expect(browser.getTitle()).toEqual('Admin - Add New Data');
         //test form input mbtb_code
         element(by.css("input[name='mbtb_code']")).sendKeys('1');
         expect(element(by.css("input[name='mbtb_code']")).getAttribute('value')).toBe('1');
         //test sex dropdown
         /*$('[name="sex"]').element(by.cssContainingText('option','Female')).click();*/

         //test age
         element(by.css("input[name='age']")).sendKeys('1');
         expect(element(by.css("input[name='age']")).getAttribute('value')).toBe('1');
         //test race
         element(by.css("input[name='race']")).sendKeys('1');
         expect(element(by.css("input[name='race']")).getAttribute('value')).toBe('1');
         //clinical diagnosis
         element(by.css("input[name='clinical_diagnosis']")).sendKeys('1');
         expect(element(by.css("input[name='clinical_diagnosis']")).getAttribute('value')).toBe('1');
         //duration
         element(by.css("input[name='duration']")).sendKeys('1');
         expect(element(by.css("input[name='duration']")).getAttribute('value')).toBe('1');

         //test clinical detail
         element(by.css("textarea[name='clinical_details']")).sendKeys('1');
         expect(element(by.css("textarea[name='clinical_details']")).getAttribute('value')).toBe('1');
         //
         element(by.css("input[name='cause_of_death']")).sendKeys('1');
         expect(element(by.css("input[name='cause_of_death']")).getAttribute('value')).toBe('1');
         //PIM
         element(by.css("input[name='postmortem_interval']")).sendKeys('1');
         expect(element(by.css("input[name='postmortem_interval']")).getAttribute('value')).toBe('1');
         //brain weight
         element(by.css("input[name='brain_weight']")).sendKeys('1');
         expect(element(by.css("input[name='brain_weight']")).getAttribute('value')).toBe('1');
         //TiF
         element(by.css("input[name='time_in_fix']")).sendKeys('1');
         expect(element(by.css("input[name='time_in_fix']")).getAttribute('value')).toBe('1');
         //test neuropathology_summary
         element(by.css("textarea[name='neuropathology_summary']")).sendKeys('1');
         expect(element(by.css("textarea[name='neuropathology_summary']")).getAttribute('value')).toBe('1');
         //gross
         element(by.css("textarea[name='neuropathology_gross']")).sendKeys('1');
         expect(element(by.css("textarea[name='neuropathology_gross']")).getAttribute('value')).toBe('1');
         //micro
         element(by.css("textarea[name='neuropathology_microscopic']")).sendKeys('1');
         expect(element(by.css("textarea[name='neuropathology_microscopic']")).getAttribute('value')).toBe('1');
         //cerad
         element(by.css("input[name='cerad']")).sendKeys('1');
         expect(element(by.css("input[name='cerad']")).getAttribute('value')).toBe('1');
         //braak_stage
         element(by.css("input[name='braak_stage']")).sendKeys('1');
         expect(element(by.css("input[name='braak_stage']")).getAttribute('value')).toBe('1');
         //khachaturian
         element(by.css("input[name='khachaturian']")).sendKeys('1');
         expect(element(by.css("input[name='khachaturian']")).getAttribute('value')).toBe('1');
         //abc
         element(by.css("input[name='abc']")).sendKeys('1');
         expect(element(by.css("input[name='abc']")).getAttribute('value')).toBe('1');
         //test by selecting second option
         var desiredOption = element.all(by.tagName('option')).get(1);
         desiredOption.click();

     });

     //log out after all
    afterAll(function(){
        element(by.id("logout")).click();
    });


});
