// To get id from selected checkbox and send a patch request to revert status
$('#revert_tissue_request_btn').click(function(e){
  // fetching selected checkbox's id from view
  let requests_ids = get_checkbox_values();

  // patch request for sending request_ids, email_data to controller
  let post_request = $.post( "/revert_archive_tissue_requests", {requests_ids: requests_ids}, function(data, status) {
    if (data === 'approved'){
      // display alert on suceess and reload window
      alert("Your selected requests are reverted.");
      location.reload();
    }
    else {
      alert("Something went wrong, Please try again.");
    }

  });

  // display error msg if no checkbox is selected
  post_request.fail(function(status) {
    alert( "Please select at least one request.");
  });

});
