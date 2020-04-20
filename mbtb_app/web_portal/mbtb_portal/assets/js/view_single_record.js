var view_single_record = angular.module("view_single_record_app", []);

view_single_record.controller("view_single_record_controller", ['$scope', '$window', '$http', function ($scope, $window, $http) {

    // binding data to angular variable from ejs view
    $scope.details = $window.mbtb_detailed_data;

    // on-click for delete button
    $scope.delete_button = function () {
      if (confirm("This action will delete data. Are you sure?")) {
        let url = '/delete_data/' + $scope.details.prime_details_id + '/';

        // DELETE request to sails controller
        $http({
          method: 'DELETE',
          url: url
        }).then(function successCallback(response) {
          if (response.data === 'Success'){
            $window.location.href = '/admin_view_data';
          }
          else {
            alert("Something went wrong, Please try again.");
          }
        });
      }
  }

  }]);

// For image files navigation
var dropdown = document.getElementsByClassName("dropdown-btn");
var i;

for (i = 0; i < dropdown.length; i++) {
  dropdown[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var dropdownContent = this.nextElementSibling;
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
}

