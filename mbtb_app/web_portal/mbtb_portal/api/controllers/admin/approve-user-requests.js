var generator = require('generate-password');
const request = require('request');

module.exports = {


  friendlyName: 'Approve user requests',


  description: 'Approve new account requests and generate random password',


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
    let requests_ids = inputs.requests_ids;
    let email_data = inputs.email_data;
    let error_msg = '';


    for (i=0; i<requests_ids.length; i++){

      let url = 'http://127.0.0.1:8000/list_new_users/' + requests_ids[i] + '/';
      let payload = {
        pending_approval: "N",
        password_hash: generator.generate({
          length: 15,
          numbers: true
        })
      };

      request.patch({url: url, body: payload, json: true,
          'headers': {
            'content-type': 'application/json',
            'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
          }
        },
        function optionalCallback(err, httpResponse, body) {
          if (err && httpResponse.statusCode !== 200) {
            error_msg = 'Error';
            return exits.success("error");
          }
          else {
            console.log("New user request approved, ID: ", requests_ids[i-1]);
          }
        });

      if (error_msg !== 'Error'){

        // sending confirmation email to users
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
