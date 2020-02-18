var admin_edit_data = angular.module("admin_edit_data_app", []);

admin_edit_data.controller("admin_edit_data_controller", ['$scope', '$window', function ($scope, $window) {

  // binding data to angular variable from ejs view
  $scope.details = $window.mbtb_detailed_data;

}]);


