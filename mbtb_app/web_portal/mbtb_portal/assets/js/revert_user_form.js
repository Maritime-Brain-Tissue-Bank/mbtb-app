$('#revert_suspended_user_btn').click(function (e) {

  // fetching selected checkbox's id from view
  let requests_ids = get_checkbox_values();

  var hidden_input = document.getElementById('requests_ids');
  hidden_input.value = [requests_ids];

  //validate form only when at least one checkbox is checked
  $("#suspended_users_form").submit(function(e) {
    if(!$('input[type=checkbox]:checked').length) {
      alert("Please select at least one account.");
      //stop the form from submitting
      return false;
    }
    return true;
  });

});
