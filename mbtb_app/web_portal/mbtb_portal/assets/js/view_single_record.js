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

// This method gets the file name from ejs view (data-file-name) attribute and send a request to sails controller for image url
function displayImage(image) {
  var filename = image.getAttribute('data-file-name');

  // show loader with trasperent background
  $('.loader_wrapper').show();
  $('.loader').show();

  $.get({
    url: '/admin_get_image',
    data: {filename: filename},
    success: function(response){

      // hide the loader
      $('.loader').hide();
      $('.loader_wrapper').hide();
      openImageViewer(response.file_url);

    },

    })
    .fail(function () {
      alert("Something went wrong in rendering image, Please try again!");
      location.reload();
    });

}

// for users only
// This method gets the file name from ejs view (data-file-name) attribute and send a request to sails controller for image url
function userDisplayImage(image) {
  var filename = image.getAttribute('data-file-name');

  // show loader with trasperent background
  $('.loader_wrapper').show();
  $('.loader').show();

  $.get({
    url: '/get_image',
    data: {filename: filename},
    success: function(response){

      // hide the loader
      $('.loader').hide();
      $('.loader_wrapper').hide();
      openImageViewer(response.file_url);
    },

  })
    .fail(function () {
      alert("Something went wrong in rendering image, Please try again!");
      location.reload();
    });

}


// Open image viewer
function openImageViewer(file_url){

  // image source
  let image_item = [{
    src: file_url
  }];

  // options for image viewer - set toolbar buttons
  let image_options = {
    footToolbar: ['fullscreen', 'zoomIn','zoomOut', 'actualSize','rotateRight']
  };

  var viewer = new PhotoViewer(image_item, image_options);
}


// disable context menu on this window
document.addEventListener('contextmenu', function(e) {
  e.preventDefault();
});


// detect key press and disable developer tools, print, save via key press
document.onkeydown = function(e) {
  if(e.key === 'F12') {
    return false;
  }
  if((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === ('i' || 'I')) {
    return false;
  }
  if((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === ('c' || 'C')) {
    return false;
  }
  if((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === ('j' || 'J')) {
    return false;
  }
  if((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === ('u' || 'U')) {
    return false;
  }
  if((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === ('p' || 'P')) {
    return false;
  }
  if((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === ('s' || 'S')) {
    return false;
  }
}
