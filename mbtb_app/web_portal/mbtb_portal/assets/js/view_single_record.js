var app = angular
  .module("view_single_record_app", [])
  .controller("view_single_record_controller", function ($scope, $window) {

    $scope.details = $window.mbtb_detailed_data;

  });

