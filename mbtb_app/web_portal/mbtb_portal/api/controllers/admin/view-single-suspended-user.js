const request = require('request');

module.exports = {


  friendlyName: 'Get single suspended user',


  description: 'This controller fetched details for single suspended user.',


  inputs: {

    id: {
      description: 'The id of a user for detail view',
      type: 'number',
      required: true
    },

  },


  exits: {

    success: {
      viewTemplatePath: 'pages/admin_view_single_suspended_user',
      description: 'On success, return to `admin_view_single_suspended_user` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function ({id}, exits) {

    // get request to retrieve single suspended user data for single id from api with admin auth token
    let url = sails.config.custom.user_api_url + 'suspended_users/' + id + '/';
    request.get(url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err}); // log error to server console
        }
        else {
          let response = JSON.parse(body);

          // return retrieved data to template in form of dictionary with key: `detailed_data`
          return exits.success({detailed_data: response});
        }
      });


  }


};
