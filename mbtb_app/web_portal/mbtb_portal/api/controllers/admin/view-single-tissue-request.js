const request = require('request');

module.exports = {


  friendlyName: 'View single tissue request',


  description: 'Retrieve single tissue request from api',


  inputs: {

    id: {
      description: 'The id of the tissue_request for detail view',
      type: 'number',
      required: true
    },

  },


  exits: {

    success: {
      viewTemplatePath: 'pages/admin_view_single_tissue_request',
      description: 'On success, return to `admin_view_single_tissue_request` template',
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


  fn: async function ({id}, exits) {

    // get request to retrieve detailed mbtb data for single id from api with admin auth token
    let url = sails.config.custom.data_api_url + 'get_new_tissue_requests/' + id + '/';
    request.get(url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({
            'error_controller': 'admin/view-single-tissue-request',
            'error_msg': err
          }); // log error to server console
          return exits.error_response({'msg_title': 'Error', 'msg_body': sails.config.custom.api_down_error_msg});
        }
        else {
          var response = JSON.parse(body);

          // return retrieved data to template in form of dictionary with key: `detailed_data`
          return exits.success({detailed_data: response});
        }
      });


  }


};
