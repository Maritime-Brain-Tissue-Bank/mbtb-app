# Test

using [protractor](https://www.protractortest.org/#/) for angular testing



#### Set up

```
npm install -g protractor
```

#### Update webdriver-manager
```
webdriver-manager update
```

#### Start server

```
webdriver-manager start
```

#### Configuring browsers
```
browser setup is within capabilities object in config file. The default browser used for the test is Chrome.
```

#### Using other browsers
```
To use browsers other than Chrome, change the browser name in capabilities object in config file.
```
#### Run the test (admin)

```
protractor conf.js --suite admin_add_new_data,admin_view_data_table,view_single_record
```

#### Run the test (user)

```
protractor conf.js --suite view_data_table
```

