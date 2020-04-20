var view_single_current_user = angular.module("view_single_current_user_app", []);

view_single_current_user.controller("view_single_current_user_controller",
  ['$scope', '$window', '$http', function ($scope, $window, $http) {

    // binding data to angular variable from ejs view
    $scope.details = $window.single_current_user;

  }]);






