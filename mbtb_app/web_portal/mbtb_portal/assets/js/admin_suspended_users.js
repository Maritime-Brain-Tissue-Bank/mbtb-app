// To get id from selected checkbox and send a patch request to revert suspended users
$('#revert_suspended_user_btn').click(function(e){
  // fetching selected checkbox's id from view
  let requests_ids = get_checkbox_values();

  // patch request for sending request_ids to controller
  let post_request = $.post( "/revert_suspended_user", {requests_ids: requests_ids}, function(data, status) {
    if (data === 'Success'){
      // display alert on success and reload window
      alert("Your selected user accounts are reverted to normal state.");
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
