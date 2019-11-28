const request = require('request');

module.exports = {


  friendlyName: 'Deny user requests',


  description: 'Deny new account requests and update users with follow-up email',


  inputs: {
    requests_ids:{
      type: 'json',
      required: true,
      description: 'Receives selected ids from users for delete request'
    },

    email_data:{
      type: 'json',
      required: true,
      description: 'Receives data i.e. email, first_name, last_name for sending email to users'
    },
  },


  exits: {

  },


  fn: async function (inputs, exits) {
    let request_ids = inputs.requests_ids;
    let email_data = inputs.email_data;
    let error_msg = '';

    for (i=0; i<request_ids.length; i++){

      // url for API
      let url = sails.config.custom.user_api_url + 'list_new_users/' + request_ids[i] + '/';

      // delete request to deny new account requests
      // along with admin auth token
      request.delete({url: url,
          'headers': {
            'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
          }
        },
        function optionalCallback(err, httpResponse, body) {
          if (err && httpResponse.statusCode !== 200) {
            error_msg = 'Error';
            return exits.success("error"); // return error response if something does wrong
          }
          else {
            // log approved request IDs
            console.log("New user request denied, ID: ", request_ids[i-1]);
          }
        });

      // if error not occurred during patch request, it goes for sending email to users
      if (error_msg !== 'Error'){

        // sending request denial email to users with email, template, template data
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
