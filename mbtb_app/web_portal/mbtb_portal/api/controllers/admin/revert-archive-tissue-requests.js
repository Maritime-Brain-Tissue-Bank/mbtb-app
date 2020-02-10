const request = require('request');

module.exports = {


  friendlyName: 'Revert archive tissue requests to new requests',


  description: `It reverts state of archive tissue requests to new tissue requests.`,


  inputs: {
    requests_ids:{
      type: 'json',
      required: true,
      description: 'Receives selected ids from users for patch request'
    },

  },


  exits: {

  },


  fn: async function (inputs, exits) {
    let requests_ids = inputs.requests_ids;

    // looping through received ids for tissue requests
    for (i=0; i<requests_ids.length; i++){

      // url for API
      let url = sails.config.custom.data_api_url + 'get_archive_tissue_requests/' + requests_ids[i] + '/';
      let payload = {
        pending_approval: "Y",
      };

      // patch request for updating following fields: `pending_approval`
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
              'error_controller': 'admin/revert-archive-tissue-requests',
              'error_msg': err
            }); // log error to server console
            return exits.error_response({'msg_title': 'Error', 'msg_body': sails.config.custom.api_down_error_msg});
          }
          else {
            // log approved request IDs
            console.log("Archived tissue request reverted, ID: ", requests_ids[i-1]);
          }
        });

    }
    return exits.success("approved");
  }


};
