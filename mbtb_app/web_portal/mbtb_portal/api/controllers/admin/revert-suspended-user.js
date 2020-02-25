const request = require('request');

module.exports = {


  friendlyName: 'Revert suspended user',


  description: 'It reverts the status of suspended users, change back them to normal state',


  inputs: {
    requests_ids:{
      type: 'json',
      required: true,
      description: 'Receives selected ids from admin for patch request'
    },
  },


  exits: {

  },


  fn: async function (inputs, exits) {
    let requests_ids = inputs.requests_ids;
    let payload = {
      suspend: "N",
    };

    // looping through received ids for tissue requests
    for (i=0; i<requests_ids.length; i++){

      // url for API
      let url = sails.config.custom.user_api_url + 'suspended_users/' + requests_ids[i] + '/';

      // patch request for updating following fields: `suspend`
      // along with admin auth token
      request.patch({url: url, body: payload, json: true,
          'headers': {
            'content-type': 'application/json',
            'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
          }
        },
        function optionalCallback(err, httpResponse, body) {
          if (err) {
            console.log({
              'error_controller': 'admin/revert-suspended-single',
              'error_msg': err
            }); // log error to server console
            return exits.error_response({'msg_title': 'Error', 'msg_body': sails.config.custom.api_down_error_msg});
          }
          else {
            // log approved request IDs
            console.log("Suspended user account reverted to normal state with ID: ", requests_ids[i-1]);
          }
        });

    }
    return exits.success("approved");
  }


};
