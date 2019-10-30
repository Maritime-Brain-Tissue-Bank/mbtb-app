// To get id from selected checkbox and send a patch request to approve status
$('#accept_request_btn').click(function(e){
  var requests_ids = [];
  var data_length = document.getElementById('data_length').value;

  for ( var j = 0; j < data_length; j++) {
    var check=$('input:checkbox[name=checkbox'+j+']').is(':checked');
    if(check==true)
      requests_ids.push($('input:checkbox[name=checkbox'+j+']').val());
  }

  // patch request
  $.post( "/approve_user_requests", {requests_ids: requests_ids}, function(data, status) {
    if (data === 'approved'){
      alert("Your selected requested are approved.");
      location.reload();
    }
    else {
      alert("Something went wrong, Please try again.");
    }

  }).
    fail(function(status) {
      alert( "Please select at least one request.");
      })
    ;
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

