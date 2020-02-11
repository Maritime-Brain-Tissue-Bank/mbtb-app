let view_single_tissue_request = angular.module("view_single_tissue_request_app", []);

view_single_tissue_request.controller("view_single_tissue_request_controller", ['$scope', '$window', '$http', function ($scope, $window, $http) {

  // binding data to angular varible from ejs view
  $scope.details = $window.tissue_request_data;

  // on-click for approve button
  $scope.approve_single_tissue_req_button = function () {

    let url = '/approve_tissue_requests/';
    let requests_ids = [$scope.details.tissue_requests_id];

    // post request to sails controller
    $http({
      method: 'POST',
      url: url,
      data: {requests_ids: requests_ids},
    }).then(function successCallback(response) {
      if (response.data === 'approved'){
        $window.location.href = '/get_new_tissue_requests';
      }
      else {
        alert("Something went wrong, Please try again.");
      }
    });

  }

}]);


