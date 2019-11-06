var generator = require('generate-password');
const request = require('request');

module.exports = {


  friendlyName: 'Approve user requests',


  description: `Approve new user account requests and generate random password.
    Also it sends a confirmation email to users with random  generated password`,


  inputs: {
    requests_ids:{
      type: 'json',
      required: true,
      description: 'Receives selected ids from users for patch request'
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
    let requests_ids = inputs.requests_ids;
    let email_data = inputs.email_data;
    let error_msg = '';


    for (i=0; i<requests_ids.length; i++){

      // url for API
      let url = 'https://mbtb-users.herokuapp.com/list_new_users/' + requests_ids[i] + '/';
      let payload = {
        pending_approval: "N",
        password_hash: generator.generate({
          length: 15,
          numbers: true
        })
      };

      // patch request for updating following fields: `pending_approval`, `password_hash`
      // along with admin auth token
      request.patch({url: url, body: payload, json: true,
          'headers': {
            'content-type': 'application/json',
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
            console.log("New user request approved, ID: ", requests_ids[i-1]);
          }
        });

      // if error not occurred during patch request, it goes for sending email to users
      if (error_msg !== 'Error'){

        // sending confirmation email to users with email, template, template data
        await sails.helpers.sendTemplateEmail.with({
          to: email_data[i].email,
          subject: `Welcome to MBTB`,
          template: 'approve_requests',
          templateData: {
            recipient_name: email_data[i].first_name + ' ' + email_data[i].last_name,
            password: payload.password_hash
          }
        });

        console.log("Email sent to: " + email_data[i].email + " for user account request approval");
      }

    }
    return exits.success("approved");
  }


};
