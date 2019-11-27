var myApp = angular.module('view_data_table_app', ['dataGrid', 'pagination']);

myApp.controller('view_data_table_controller', ['$scope', '$filter', '$window', function ($scope, $filter, $window) {

  $scope.gridOptions = {
    data: [],
  };

  $scope.gridActions1 = {};

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

  // Once search button is pressed, filters are called
  $scope.submit_search_fields = function(){

    if (document.getElementById("test").style.display === "none")
      document.getElementById("test").style.display="block";

    // filtering:
    $scope.filtered_data.data = $filter('filter')($scope.gridOptions.data, {
      sex: $scope.search_fields.sex, age: $scope.search_fields.age, preservation_method: $scope.search_fields.preservation_method,
      tissue_type: $scope.search_fields.tissue_type, neuro_diagnosis_id: $scope.search_fields.neuropathology_diagnosis,
      clinical_diagnosis: $scope.search_fields.clinical_diagnosis
    });

    /*
      To Do: refactor below 3 custom filter for range, `range_filter` should be called once only
    */

    // filtering: time_in_fix
    $scope.filtered_data.data = $filter('range_filter')($scope.filtered_data.data, {
      field_name: 'time_in_fix', min_value: $scope.search_fields.tif_min,
      max_value: $scope.search_fields.tif_max
    });

    // filtering: postmortem_interval
    $scope.filtered_data.data = $filter('range_filter')($scope.filtered_data.data, {
      field_name: 'postmortem_interval', min_value: $scope.search_fields.pmi_min,
      max_value: $scope.search_fields.pmi_max
    });

    // filtering: age
    $scope.filtered_data.data = $filter('range_filter')($scope.filtered_data.data, {
      field_name: 'age', min_value: $scope.search_fields.age_min,
      max_value: $scope.search_fields.age_max
    });

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




