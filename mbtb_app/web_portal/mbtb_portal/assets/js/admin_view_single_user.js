var view_single_current_user = angular.module("view_single_current_user_app", []);

view_single_current_user.controller("view_single_current_user_controller", ['$scope', '$window', '$http', function ($scope, $window, $http) {

  // binding data to angular variable from ejs view
  $scope.details = $window.single_current_user;

  // on-click for suspend button
  $scope.suspend_single_user = function () {
    if (confirm("This action will suspend current user. Are you sure?")) {
      let url = '/suspend_single_user/';

      // DELETE request to sails controller
      $http({
        method: 'POST',
        url: url,
        data: {requests_ids: [$scope.details.id]}
      }).then(function successCallback(response) {
        if (response.data === 'Success'){
          alert("The selected user account is suspended.");
          $window.location.href = '/view_current_users';
        }
        else {
          alert("Something went wrong, Please try again.");
        }
      });
    }
  }

}]);


