# Test

using [protractor](https://www.protractortest.org/#/) for angular testing



####Set up

```
npm install -g protractor
```

####Start server

```
webdriver-manager start
```

####Run the test (admin side)

```
protractor conf.js --suite admin_add_new_data,admin_view_data_table,view_single_record
```

####Run the test (user)

```
protractor conf.js --suite view_data_table
```

