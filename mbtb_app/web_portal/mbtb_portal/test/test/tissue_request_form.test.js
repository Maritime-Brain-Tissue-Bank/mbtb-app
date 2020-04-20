describe('User request tissue', function () {

  beforeAll(function () {
    browser.get('http://localhost:1337/tissue_requests_form');
    browser.waitForAngularEnabled(false);
    element(by.css("input[name='user_email']")).sendKeys('yc441486@dal.ca');
    element(by.css("input[name='user_password']")).sendKeys('UX8Ktap36lHCpFt');
    element(by.id("submit_btn")).click();
  });
  //test tissue request form
  it('User - tissue request', function () {
    browser.get('http://localhost:1337/tissue_requests_form');
    expect(browser.getTitle()).toEqual('Tissue Requests');
    element(by.css("input[name='title']")).sendKeys('1');
    expect(element(by.css("input[name='title']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='first_name']")).sendKeys('1');
    expect(element(by.css("input[name='first_name']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='last_name']")).sendKeys('1');
    expect(element(by.css("input[name='last_name']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='email']")).sendKeys('user@testemail.com');
    expect(element(by.css("input[name='email']")).getAttribute('value')).toBe('user@testemail.com');

    element(by.css("input[name='institution']")).sendKeys('1');
    expect(element(by.css("input[name='institution']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='department_name']")).sendKeys('1');
    expect(element(by.css("input[name='department_name']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='city']")).sendKeys('1');
    expect(element(by.css("input[name='city']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='province']")).sendKeys('1');
    expect(element(by.css("input[name='province']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='postal_code']")).sendKeys('1');
    expect(element(by.css("input[name='postal_code']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='phone_number']")).sendKeys('1');
    expect(element(by.css("input[name='phone_number']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='fax_number']")).sendKeys('1');
    expect(element(by.css("input[name='fax_number']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='project_title']")).sendKeys('1');
    expect(element(by.css("input[name='project_title']")).getAttribute('value')).toBe('1');

    element(by.css("textarea[name='source_of_funding']")).sendKeys('1');
    expect(element(by.css("textarea[name='source_of_funding']")).getAttribute('value')).toBe('1');

    element(by.css("textarea[name='abstract']")).sendKeys('1');
    expect(element(by.css("textarea[name='abstract']")).getAttribute('value')).toBe('1');

    element(by.css("input[name='agree_terms_checkbox']")).click();
    expect(element(by.css("input[name='agree_terms_checkbox']")).getAttribute('checked')).toBeTruthy();


    //test whether agree_terms_checkbox is required
    expect(element(by.css("input[name='agree_terms_checkbox']")).getAttribute("required")).toBe("true");
  });


  afterAll(function () {
    element(by.id("user_logout")).click();
  });


});

