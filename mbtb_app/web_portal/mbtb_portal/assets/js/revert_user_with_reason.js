var revert_user_with_reason = angular.module("revert_user_with_reason_app", []);

revert_user_with_reason.controller("revert_user_with_reason_controller",
  ['$scope', '$window', '$http', function ($scope, $window, $http) {

    //binding data to angular variable from ejs view
    $scope.requests_ids_ = $window.requests_ids_;
    $scope.revert_reason = "";

    // on-click of confirm button
    $scope.confirmClick = function () {
      if (confirm("This action will revert a suspended user. Are you sure?")) {
        let url = '/revert_user_with_reason/';

        // POST request to sails controller
        $http({
          method: 'POST',
          url: url,
          data: {
            requests_ids: [$scope.requests_ids_],
            revert_reason: $scope.revert_reason
          }
        }).then(function successCallback(response) {
          if (response.data === 'Success') {
            alert("The selected user account is reverted to normal state.");
            $window.location.href = '/view_suspended_users';
          } else {
            alert("Something went wrong, Please try again.");
          }
        });
      }

    }

  }]);
