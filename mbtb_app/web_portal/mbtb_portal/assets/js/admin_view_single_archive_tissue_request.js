let view_single_archive_tissue_request = angular.module("view_single_archive_tissue_request_app", []);

view_single_archive_tissue_request.controller("view_single_archive_tissue_request_controller", ['$scope', '$window', '$http', function ($scope, $window, $http) {

  // binding data to angular variable from ejs view
  $scope.details = $window.archive_tissue_request_data;

  // on-click for approve button
  $scope.revert_single_tissue_req_btn = function () {

    let url = '/revert_archive_tissue_requests/';
    let requests_ids = [$scope.details.tissue_requests_id];

    // post request to sails controller
    $http({
      method: 'POST',
      url: url,
      data: {requests_ids: requests_ids},
    }).then(function successCallback(response) {
      if (response.data === 'approved'){
        // display alert on success and reload window
        alert("Your selected request is reverted.");
        $window.location.href = '/get_archive_tissue_requests';
      }
      else {
        alert("Something went wrong, Please try again.");
      }
    });
  };

  // on-click for delete button
  $scope.delete_single_archive_tissue_req_btn = function () {
    if (confirm("This action will delete given archived tissue request. Are you sure?")) {
      let url = '/delete_archive_tissue_requests/';
      let requests_ids = [$scope.details.tissue_requests_id];

      // post request to sails controller
      $http({
        method: 'POST',
        url: url,
        data: {requests_ids: requests_ids},
      }).then(function successCallback(response) {
        if (response.data === 'completed') {
          // display alert on success and redirect window
          alert("Your selected request is deleted.");
          $window.location.href = '/get_archive_tissue_requests';
        }
        else {
          alert("Something went wrong, Please try again.");
        }
      });
    }
  };

}]);


