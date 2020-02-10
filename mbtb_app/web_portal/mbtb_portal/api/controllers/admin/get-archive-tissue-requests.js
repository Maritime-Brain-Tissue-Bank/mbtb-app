const request = require('request');

module.exports = {


  friendlyName: 'Admin - Get archive tissue requests',


  description: 'This controller is to fetch archived tissue requests and display it.',


  inputs: {

  },


  exits: {
    success: {
      viewTemplatePath: 'pages/admin_archive_tissue_requests',
      description: 'On success, redirect admin to `admin_arhive_tissue_requests` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    },

    error_response: {
      responseType: 'view',
      viewTemplatePath: 'pages/message',
      description: 'return view if APIs are down.'
    }

  },


  fn: async function (inputs, exits) {
    let url = sails.config.custom.data_api_url + 'get_archive_tissue_requests/';

    // get request to retrieve registration requests from api with admin auth token
    request.get(url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({
            'error_controller': 'admin/get-archive-tissue-requests',
            'error_msg': err
          }); // log error to server console
          return exits.error_response({'msg_title': 'Error', 'msg_body': sails.config.custom.api_down_error_msg});
        }
        else {
          const response = JSON.parse(body);
          // return retrieved data to template in form of dictionary with key: `data`
          return exits.success({data: response});
        }
      });

  }


};
