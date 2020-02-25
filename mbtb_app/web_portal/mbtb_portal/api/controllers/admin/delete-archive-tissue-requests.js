const request = require('request');

module.exports = {


  friendlyName: 'Delete archived tissue requests',


  description: 'This controller is to delete archived tissue requests.',


  inputs: {
    requests_ids:{
      type: 'json',
      required: true,
      description: 'Receives selected ids from users for delete request'
    },

  },


  exits: {

  },


  fn: async function (inputs, exits) {
    let request_ids = inputs.requests_ids;

    for (i=0; i<request_ids.length; i++){

      // url for API
      let url = sails.config.custom.data_api_url + 'get_archive_tissue_requests/' + request_ids[i] + '/';

      // delete request to remove archived tissue requests
      // along with admin auth token
      request.delete(
        {url: url,
          'headers': {
            'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
          }
        },
        function optionalCallback(err, httpResponse, body) {
          if (err) {
            console.log({
              'error_controller': 'admin/delete-archive-tissue-requests',
              'error_msg': err
            }); // log error to server console
            return exits.error_response({'msg_title': 'Error', 'msg_body': sails.config.custom.api_down_error_msg});
          }
          else {
            // log approved request IDs
            console.log("Tissue request deleted, ID: ", request_ids[i-1]);
          }
        });
    }
    return exits.success("completed");

  }


};
