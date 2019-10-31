var myApp = angular.module('view_data_table_app', ['dataGrid', 'pagination']);

myApp.controller('view_data_table_controller', ['$scope', '$filter', function ($scope, $filter) {

  // sample data
  var messages = JSON.stringify([
    {
      "mbtb_code": 1234,
      "sex": "male",
      "age": 50,
      "postmortem_interval": "1 day",
      "time_in_fix": 56,
      "neuro_diagnosis": "sadad adasfaf asdasfas sadad adasfaf asdasfas sadad adasfaf asdasfas",
      "tissue_type": "fixed",
      "storage_method": "frozen",
    },{
      "mbtb_code": 1234567,
      "sex": "male",
      "age": 79,
      "postmortem_interval": "1 day",
      "time_in_fix": 12,
      "neuro_diagnosis": "sadad adasfaf asdasfas",
      "tissue_type": "fixed",
      "storage_method": "frozen",
    },
    {
      "mbtb_code": 123456,
      "sex": "male",
      "age": 45,
      "postmortem_interval": "1 day",
      "time_in_fix": 24,
      "neuro_diagnosis": "sadad adasfaf asdasfas",
      "tissue_type": "fixed",
      "storage_method": "frozen",
    }]);

  $scope.messages = JSON.parse(messages);

  $scope.gridOptions = {
    data: []
  };

  $scope.gridActions1 = {};

  $scope.gridOptions.data = $scope.messages;

  $scope.exportToCsv = function (currentData) {
    var exportData = [];
    currentData.forEach(function (item) {
      exportData.push({
        'Code': item.code,
        'Date Placed': $filter('date')(item.placed, 'shortDate'),
        'Status': item.statusDisplay,
        'Total': item.total.formattedValue
      });
    });
    JSONToCSVConvertor(exportData, 'Export', true);
  }
}]);
