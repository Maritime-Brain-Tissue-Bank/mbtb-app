const request = require('request');

module.exports = {


  friendlyName: 'Deny user requests',


  description: 'Deny new account requests',


  inputs: {
    requests_ids:{
      type: 'json',
      required: true
    },

    email_data:{
      type: 'json',
      required: true
    },
  },


  exits: {

  },


  fn: async function (inputs, exits) {
    let request_ids = inputs.requests_ids;
    let email_data = inputs.email_data;
    let error_msg = '';

    for (i=0; i<request_ids.length; i++){

      var url = 'https://mbtb-users.herokuapp.com/list_new_users/' + request_ids[i] + '/';

      request.delete({url: url,
          'headers': {
            'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
          }
        },
        function optionalCallback(err, httpResponse, body) {
          if (err && httpResponse.statusCode !== 200) {
            error_msg = 'Error';
            return exits.success("error");
          }
          else {
            console.log("New user request denied, ID: ", request_ids[i-1]);
          }
        });

      if (error_msg !== 'Error'){

        // sending confirmation email to users
        await sails.helpers.sendTemplateEmail.with({
          to: email_data[i].email,
          subject: `New Account Request Status - MBTB Dataset`,
          template: 'deny_requests',
          templateData: {
            recipient_name: email_data[i].first_name + ' ' + email_data[i].last_name
          }
        });

        console.log("Email sent: user account request denial");
      }
    }
    return exits.success("completed");

  }


};
