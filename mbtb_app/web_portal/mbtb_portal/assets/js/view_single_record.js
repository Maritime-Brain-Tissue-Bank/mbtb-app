var view_single_record = angular.module("view_single_record_app", []);

view_single_record.controller("view_single_record_controller", ['$scope', '$window', function ($scope, $window) {

    // binding data to angular varible from ejs view
    $scope.details = $window.mbtb_detailed_data;

  }]);


