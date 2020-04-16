var suspend_user_with_reason = angular.module("suspend_user_with_reason_app", []);

suspend_user_with_reason.controller("suspend_user_with_reason_controller",
  ['$scope', '$window', '$http', function ($scope, $window, $http) {

  //binding data to angular variable from ejs view
    $scope.requests_ids_ = $window.requests_ids_;
    $scope.suspend_reason = "";

    // on-click of confirm button
    $scope.confirmClick = function () {
      if (confirm("This action will suspend a user. Are you sure?")) {
        let url = '/suspend_user_with_reason/';

        // POST request to sails controller
        $http({
          method: 'POST',
          url: url,
          data: {
            requests_ids: [$scope.requests_ids_],
            suspend_reason: $scope.suspend_reason
          }
        }).then(function successCallback(response) {
          if (response.data === 'Success') {
            alert("The selected user account is suspended.");
            $window.location.href = '/view_suspended_users';
          } else {
            alert("Something went wrong, Please try again.");
          }
        });
      }

    }

  }]);
