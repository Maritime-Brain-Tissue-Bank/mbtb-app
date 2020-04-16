$('#revert_suspended_user_btn').click(function (e) {

  // fetching selected checkbox's id from view
  let requests_ids = get_checkbox_values();

  var hidden_input = document.getElementById('requests_ids');
  hidden_input.value = [requests_ids];

});



