angular.module('myApp', ['dataGrid', 'pagination'])
  .controller('myAppController', ['$scope', '$filter', 'myAppFactory',function ($scope, $filter,myAppFactory) {


    $scope.gridOptions = {
      data: [],
      urlSync: true
    };


    $scope.gridActions1 = {};

    myAppFactory.getData().then(function (responseData) {
      $scope.gridOptions.data = responseData.data;
    });

    $scope.exportToCsv = function (currentData) {
      var exportData = [];
      currentData.forEach(function (item) {
        exportData.push({
          'MBTB Code': item.MBTB_code,
          'SEX': item.SEX,
          'AGE': item.AGE,
          'POSTMORTEM INTERVAL': item.postmortem_interval,
          'TIME IN FIX (days)':item.time_in_fix,
          'NEUROPATHOLOGICAL DIAGNOSIS':item.neuro_disease_id,
          'TISSUE TYPE':item.tissue_type_id,
          'STORAGE METHOD':item.storage_method,
        });
      });
      JSONToCSVConvertor(exportData, 'Export', true);
    }

  }])
  .factory('myAppFactory', function ($http) {
    return {
      getData: function () {
        return $http({
          method: 'GET',
          url: 'https://angular-data-grid.github.io/demo/data.json'
        });
      }
    }


  });
