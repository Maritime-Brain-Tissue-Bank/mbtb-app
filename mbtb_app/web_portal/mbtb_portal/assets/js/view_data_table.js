var view_data_table_app = angular.module('view_data_table_app', ['dataGrid', 'pagination']);

view_data_table_app.controller('view_data_table_controller', ['$scope', '$filter', '$window', '$http', function ($scope, $filter, $window, $http) {

  $scope.gridOptions = {
    data: [],
  };

  $scope.clear_btn = true; // for clear button, by default is is disabled

  // data binding to angular variable
  $scope.gridOptions.data = $window.mbtb_data;

  // for finding unique elements in array
  let unique = (value, index, self) => {
    return self.indexOf(value) === index
  };

  $scope.search_fields = {}; // save user choices from form
  $scope.filtered_data = {
    data : [], // save filtered data

  };

  // options for filtering with select options
  $scope.search_fields.select_options = [
    'sex', 'clinical_diagnosis', 'neuropathology_diagnosis', 'preservation_method', 'tissue_type'
  ];

  // options for range filtering with min, max values
  $scope.search_fields.range_options = [
    'time_in_fix', 'postmortem_interval', 'age'
  ];

  $scope.data_mode = {
    type: 'View',
    value: 'admin_view_data'
  };

  // Once search button is pressed, filters are called
  $scope.submit_search_fields = function(){

    if (document.getElementById("test").style.display === "none")
      document.getElementById("test").style.display="block";

    // ensuring if value is '' then delete that object so that all values can be displayed
    // fix for filtering with exact match
    $scope.search_fields.select_options.forEach(function (item) {
      if ($scope.search_fields[item] === ""){
        delete $scope.search_fields[item];
      }
    });

    // filtering: exact match
    $scope.filtered_data.data = $filter('filter')($scope.gridOptions.data, {
      sex: $scope.search_fields.sex, age: $scope.search_fields.age, preservation_method: $scope.search_fields.preservation_method,
      tissue_type: $scope.search_fields.tissue_type, neuro_diagnosis_id: $scope.search_fields.neuropathology_diagnosis,
      clinical_diagnosis: $scope.search_fields.clinical_diagnosis
    }, true);

    // filtering: using custom range filter for time_in_fix, age, postmortem_interval
    $scope.search_fields.range_options.forEach(function (item) {
      $scope.filtered_data.data = $filter('range_filter')($scope.filtered_data.data,{
        field_name: item, min_value: $scope.search_fields[item + '_min'],
        max_value: $scope.search_fields[item + '_max']
      });
    });

    if ($scope.data_mode.type === 'Edit'){
      $scope.data_mode.value = 'edit_data';
    }
    else {
      $scope.data_mode.value = 'admin_view_data';
    }

    $scope.clear_btn = false; // enable clear button
  };

  // clear filtered data and set table, options to default view
  $scope.clear_filter = function(){
    $scope.filtered_data.data = $scope.gridOptions.data;

    // setting select options to default value
    $scope.search_fields.select_options.forEach(function (item) {
      $scope.search_fields[item] = "";
    });

    // setting input fields to null value
    $scope.search_fields.range_options.forEach(function (item) {
      $scope.search_fields[item + '_min'] = null;
      $scope.search_fields[item + '_max'] = null;
    });

    $scope.data_mode.type = 'View';
    $scope.data_mode.value = 'admin_view_data';

    $scope.clear_btn = true; // disable clear button
  };


  // Download csv file function
  $scope.download_csv_file = function (download_mode){

    let url = '/download_data/';
    let export_data = [];
    let payload = [];
    let filename = 'MBTB Data';

    // post request to sails controller
    let post_request = function (url, payload, filename) {
      $http({
        method: 'POST',
        url: url,
        data: payload,
      }).then(function successCallback(response) {
        if (response.data.operation === 'completed') {

          // user prompt to download the csv file, here received data is in json
          JSONToCSVConvertor(response.data.data, filename, true);
        } else {
          alert("Something went wrong, Please try again.");
        }
      });
    };

    // validating download mode
    if (download_mode === 'all'){
      payload = {
        download_mode: download_mode
      };
      post_request(url, payload, filename);
    }
    else if (download_mode === 'filtered'){

      // pushing filtered mbtb_code values in export_data
      $scope.filtered_data.data.forEach(function (item) {
        export_data.push({
          'mbtb_code': item.mbtb_code,
        });
      });

      // preparing payload data
      payload = {
        download_mode: download_mode,
        input_mbtb_codes: export_data
      };

      filename = 'Filtered MBTB data';
      post_request(url, payload, filename);
    }
    else {
      alert("Something went wrong, please try again.??");
      $window.location.reload();
    }

  };
}]);

// custom filter to find values between range
view_data_table_app.filter('range_filter', function () {
  return function (data, options) {
    // default min and max values are 0 and 1000
    let min_value = parseInt(options.min_value) || 0 ;
    let max_value = parseInt(options.max_value) || 1000;

    if (options.field_name !== undefined){
      return data.filter((item) => (item[options.field_name] >= min_value && item[options.field_name] <= max_value)
    )}
  }
});




