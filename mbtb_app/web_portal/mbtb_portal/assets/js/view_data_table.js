var myApp = angular.module('view_data_table_app', ['dataGrid', 'pagination']);

myApp.controller('view_data_table_controller', ['$scope', '$filter', '$window', function ($scope, $filter, $window) {

  $scope.gridOptions = {
    data: [],
  };

  $scope.clear_btn = true; // for clear button, by default is is disabled

  // data binding to angular variable
  $scope.gridOptions.data = $window.mbtb_data;

  // for finding unique elemenets in array
  let unique = (value, index, self) => {
    return self.indexOf(value) === index
  };

  // clinical diagnosis
  $scope.clinical_diagnosis = [];
  $scope.gridOptions.data.forEach(function (item) {
    if (item.clinical_diagnosis.length > 0){
      $scope.clinical_diagnosis.push(item.clinical_diagnosis);
    }
  });
  $scope.clinical_diagnosis = $scope.clinical_diagnosis.filter(unique);

  // Neuropathological diagnosis
  $scope.neuropathology_diagnosis = [];
  $scope.gridOptions.data.forEach(function (item) {
    $scope.neuropathology_diagnosis.push(item.neuro_diagnosis_id);
  });
  $scope.neuropathology_diagnosis = $scope.neuropathology_diagnosis.filter(unique);

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

    $scope.clear_btn = true; // disable clear button
  };

  // exporting data or filtered data to csv
  $scope.exportToCsv = function (currentData) {
    var export_data = [];
    currentData.forEach(function (item) {
      export_data.push({
        'MBTB Code': item.mbtb_code,
        'Sex': item.sex,
        'Age': item.age,
        'Postmortem Interval': item.postmortem_interval,
        'Time in Fix': item.time_in_fix,
        'Neuropathological Diagnosis': item.neuropathology_diagnosis,
        'Tissue Type': item.tissue_type,
        'Preservation Method': item.preservation_method,
        'Clinical Diagnosis': item.clinical_diagnosis,
        'Storage Date': item.storage_year
      });
    });
    JSONToCSVConvertor(export_data, 'Export', true);
  }
}]);

// custom filter to find values between range
myApp.filter('range_filter', function () {
  return function (data, options) {
    // default min and max values are 0 and 1000
    let min_value = parseInt(options.min_value) || 0 ;
    let max_value = parseInt(options.max_value) || 1000;

    if (options.field_name !== undefined){
      return data.filter((item) => (item[options.field_name] >= min_value && item[options.field_name] <= max_value)
    )}
  }
});




