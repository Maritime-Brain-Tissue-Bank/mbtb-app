const request = require('request');

module.exports = {


  friendlyName: 'Revert users',


  description: `It reverts users to normal state with reason.`,


  inputs: {
    requests_ids:{
      type: 'json',
      required: true,
      description: 'Receives selected ids from admin for patch request'
    },
    revert_reason:{
      type:'string',
      required:true,
      description:'Receive revert reason'
    }

  },


  exits: {

  },


  fn: async function (inputs, exits) {
    let requests_ids = inputs.requests_ids;
    let revert_reason = inputs.revert_reason;
    let payload = {
      suspend: "N",
      revert_reason: revert_reason,
    };

   /* for (i = 0; i < requests_ids.length; i++) {
      requests_ids = JSON.parse("[" + requests_ids[i] + "]");
    }*/

    requests_ids = JSON.parse("[" + requests_ids + "]");

    console.log("\n\n  **************   \n\n");
    console.log(inputs.revert_reason);
    console.log(requests_ids);

    // looping through received ids
    for (i=0; i<requests_ids.length; i++){
      //console.log("\n >>>>>>>"+requests_ids[i]+"\n");
      //console.log("\n >>>>>>>" + typeof(requests_ids[i]) + "\n");

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
              'error_controller': 'admin/revert-user-with-reason',
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
    return exits.success("Success");
  }


};
