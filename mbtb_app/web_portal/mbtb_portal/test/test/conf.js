exports.config = {
  framework: 'jasmine',
  seleniumAddress: 'http://localhost:4444/wd/hub',
  capabilities: {
    'browserName': 'chrome',
  },
  suites: {
    admin_add_new_data: 'admin_add_new_data.test.js',
    admin_view_data_table: 'admin_view_data_table.test.js',
    view_single_record: 'view_single_record.test.js',
    view_data_table: 'view_data_table.test.js',
    tissue_requests_form: 'tissue_request_form.test.js',
    admin_archive_tissue_requests:'admin_archive_tissue_requests.test.js',
    admin_view_single_archive_tissue_request:'admin_view_single_archive_tissue_request.test.js',
    admin_new_tissue_requests:'admin_new_tissue_requests.test.js',
    admin_view_single_new_tissue_request:'admin_view_single_new_tissue_request.test.js',
    admin_file_upload:'admin_file_upload.test.js',
    admin_view_current_users:'admin_view_current_users.test.js',
    admin_view_suspended_user:'admin_view_suspended_user.test.js',
    admin_view_single_user:'admin_view_single_user.test.js',
    downloaded_file:'downloaded_file.test.js'
  },

  // to handle timeout error
  // jasmineNodeOpts: {
  //   showColors: true,
  //   includeStackTrace: true,
  //   defaultTimeoutInterval: 144000,
  // }


};

