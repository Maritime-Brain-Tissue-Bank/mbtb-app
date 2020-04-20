const request = require('request');

module.exports = {


  friendlyName: 'Suspend users',


  description: `It suspends users from given list, Even controller's name say to suspend a single user but it can suspends multiple users at once.`,


  inputs: {
    requests_ids:{
      type: 'json',
      required: true,
      description: 'Receives selected ids from admin for patch request'
    },
    suspend_reason:{
      type:'string',
      required:true,
      description:'Receive suspend reason'
    }

  },


  exits: {

  },


  fn: async function (inputs, exits) {
    let requests_ids = inputs.requests_ids;
    let suspend_reason = inputs.suspend_reason;
    let payload = {
      suspend: "Y",
      suspend_reason: suspend_reason,
    };

    //convert requests_ids string to array
    requests_ids = JSON.parse("[" + requests_ids + "]");
    
    // looping through received ids
    for (i=0; i<requests_ids.length; i++){

      // url for API
      let url = sails.config.custom.user_api_url + 'current_users/' + requests_ids[i] + '/';

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
              'error_controller': 'admin/suspend-user-with-reason',
              'error_msg': err
            }); // log error to server console
            return exits.error_response({'msg_title': 'Error', 'msg_body': sails.config.custom.api_down_error_msg});
          }
          else {
            // log approved request IDs
              console.log("User suspended with ID: ", requests_ids[i-1]);

          }
        });

    }
    return exits.success("Success");
  }


};
