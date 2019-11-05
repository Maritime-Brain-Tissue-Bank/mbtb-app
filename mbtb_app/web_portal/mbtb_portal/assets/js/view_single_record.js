var view_single_record = angular.module("view_single_record_app", []);

view_single_record.controller("view_single_record_controller", ['$scope', '$window', function ($scope, $window) {

    $scope.details = $window.mbtb_detailed_data;

  }]);


