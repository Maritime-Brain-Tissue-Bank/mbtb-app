exports.config = {
    framework: 'jasmine',
    seleniumAddress: 'http://localhost:4444/wd/hub',
    capabilities: {
        'browserName': 'chrome'
    },
    suites:{
        admin_add_new_data:'admin_add_new_data.test.js',
        admin_view_data_table:'admin_view_data_table.test.js',
        view_single_record:'view_single_record.test.js',
        view_data_table:'view_data_table.test.js'
    }
};

