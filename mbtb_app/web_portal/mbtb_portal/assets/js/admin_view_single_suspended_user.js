var view_single_suspended_user = angular.module("view_single_suspended_user_app", []);

view_single_suspended_user.controller("view_single_suspended_user_controller", [
  '$scope', '$window', '$http', function ($scope, $window, $http) {

  // binding data to angular variable from ejs view
  $scope.details = $window.single_suspended_user;

  // on-click for revert button
  $scope.revert_suspended_user = function () {
    if (confirm("This action will revert suspended user to normal state. Are you sure?")) {
      let url = '/revert_suspended_user/';

      // DELETE request to sails controller
      $http({
        method: 'POST',
        url: url,
        data: {requests_ids: [$scope.details.id]}
      }).then(function successCallback(response) {
        if (response.data === 'Success'){
          alert("The selected user account is reverted.");
          $window.location.href = '/view_suspended_users';
        }
        else {
          alert("Something went wrong, Please try again.");
        }
      });
    }
  }

}]);


