// To get id from selected checkbox and send a patch request to approve status
$('#accept_request_btn').click(function(e){
  // fetching selected checkbox's id from view
  let requests_ids = get_checkbox_values();

  // fetching email data: first_name, last_name, email from selected checkbox
  let email_data = get_email_data(requests_ids);

  // patch request for sending request_ids, email_data to controller
  let post_request = $.post( "/approve_user_requests", {requests_ids: requests_ids, email_data: email_data}, function(data, status) {
    if (data === 'approved'){
      // display alert on suceess and reload window
      alert("Your selected requests are approved.");
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

// To get id from selected checkbox and send a delete request to deny status
$('#deny_request_btn').click(function(e){

// fetching selected checkbox's id from view
  var requests_ids = get_checkbox_values();

  // fetching email data: first_name, last_name, email from selected checkbox
  var email_data = get_email_data(requests_ids);

  // patch request for sending request_ids, email_data to controller
  var delete_request = $.post( "/deny_user_requests", {requests_ids: requests_ids, email_data: email_data}, function(data, status) {
    if (data === 'completed'){
      // display alert on suceess and reload window
      alert("Your selected requests are denied.");
      location.reload();
    }
    else {
      alert("Something went wrong, Please try again.");
    }

  });

  // display error msg if no checkbox is selected
  delete_request.fail(function(status) {
    alert( "Please select at least one request.");
  });
});

// For a checkbox in header to check or uncheck all remaining checkbox
function toggle_all(isChecked){
  if (isChecked){
    $("input:checkbox").each(function () {
        this.checked = true;
    });
  }
  else {
    $("input:checkbox").each(function () {
      this.checked = false;
    });
  }

}

// For fetching email, first_name, last_name from selected checkbox
// return it as array
function get_email_data(requests_ids) {
  var mbtb_data_temp = window.mbtb_data;
  var email_data = [];
  for (id of requests_ids) {
    for (i=0; i<mbtb_data_temp.length; i++){
      if (mbtb_data_temp[i].id == id){
        email_data.push({
          'email': mbtb_data_temp[i].email,
          'first_name': mbtb_data_temp[i].first_name,
          'last_name': mbtb_data_temp[i].last_name,
        })
      }
    }
  }
  return email_data;
}

// For getting mbtb_data ids from selected checkbox
// return it as array
function get_checkbox_values() {
  var requests_ids = [];
  var data_length = document.getElementById('data_length').value;

  for ( var j = 0; j < data_length; j++) {
    var check = $('input:checkbox[name=checkbox'+j+']').is(':checked');
    if(check===true)
      requests_ids.push($('input:checkbox[name=checkbox'+j+']').val());
  }

  return requests_ids;
}
