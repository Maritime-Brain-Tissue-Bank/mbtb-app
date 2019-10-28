var myApp = angular.module('view_data_table_app', ['dataGrid', 'pagination']);

myApp.controller('view_data_table_controller', ['$scope', '$filter', function ($scope, $filter) {

  // sample data
  var messages = JSON.stringify([{
    "total": {
      "currencyIso": "USD",
      "priceType": "BUY",
      "value": 6100.00,
      "formattedValue": "$6,100.00"
    },
    "statusDisplay": "Valid",
    "code": "3747453",
    "placed": 1417402800000},
    {
      "total": {
        "currencyIso": "USD",
        "priceType": "BUY",
        "value": 1100.00,
        "formattedValue": "$1,100.00"
      },
      "statusDisplay": "Hold",
      "code": "3747092",
      "placed": 1398049200000
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
