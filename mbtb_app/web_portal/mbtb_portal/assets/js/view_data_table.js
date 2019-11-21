var myApp = angular.module('view_data_table_app', ['dataGrid', 'pagination']);

myApp.controller('view_data_table_controller', ['$scope', '$filter', '$window', function ($scope, $filter, $window) {

  $scope.gridOptions = {
    data: [],
    customFilters: {
      AgeMax:
        function (items, value, predicate) {
          return items.filter(function (item) {
            return value && item[predicate] ? parseInt(item[predicate]) <= parseInt(value) : true;
          });
        },
      AgeMin:
        function (items, value, predicate) {
          return items.filter(function (item) {
            return value && item[predicate] ? parseInt(item[predicate]) >= parseInt(value) : true;
          });
        },
      PMIMax:
        function (items, value, predicate) {
          return items.filter(function (item) {
            return value && item[predicate] ? parseInt(item[predicate]) <= parseInt(value) : true;
          });
        },
      PMIMin:
        function (items, value, predicate) {
          return items.filter(function (item) {
            return value && item[predicate] ? parseInt(item[predicate]) >= parseInt(value) : true;
          });
        },

      TiFMax:
        function (items, value, predicate) {
          return items.filter(function (item) {
            return value && item[predicate] ? parseInt(item[predicate]) <= parseInt(value) : true;
          });
        },
      TiFMin:
        function (items, value, predicate) {
          return items.filter(function (item) {
            return value && item[predicate] ? parseInt(item[predicate]) >= parseInt(value) : true;
          });
        },

    }
  };

  $scope.gridActions1 = {};

  // data binding to angular variable
  $scope.gridOptions.data = $window.mbtb_data;

  // exporting data or filtered data to csv
  $scope.exportToCsv = function (currentData) {
    var exportData = [];
    currentData.forEach(function (item) {
      exportData.push({
        'MBTB Code': item.mbtb_code,
        'Sex': item.sex,
        'Age': item.age,
        'Postmortem Interval': item.postmortem_interval,
        'Time in Fix': item.time_in_fix,
        'Neuropathological Diagnosis': item.neuro_diagnosis,
        'Tissue Type': item.tissue_type,
        'Storage Method': item.storage_method
      });
    });
    JSONToCSVConvertor(exportData, 'Export', true);
  }
}]);

function myFunction() {
  if (document.getElementById("test").style.display === "none")
    document.getElementById("test").style.display="block";
}




