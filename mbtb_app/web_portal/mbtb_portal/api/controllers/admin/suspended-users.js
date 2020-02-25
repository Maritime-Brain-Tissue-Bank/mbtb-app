const request = require('request');

module.exports = {


  friendlyName: 'Suspended users',


  description: 'List suspended users from api',


  inputs: {

  },


  exits: {
    success: {
      viewTemplatePath: 'pages/admin_view_suspended_users',
      description: 'On sucess, redirect admin to `admin_current_users` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function (inputs, exits) {
    let url = sails.config.custom.user_api_url + 'suspended_users/';

    // get request to retrieve registration requests from api with admin auth token
    request.get(url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err}); // log error to server console
        }
        else {
          const response = JSON.parse(body);
          // return retrieved data to template in form of dictionary with key: `data`
          return exits.success({data: response});
        }
      });

  }


};
