const request = require('request');

module.exports = {


  friendlyName: 'Register requests',


  description: 'Retrieve new user registration requests from API',


  inputs: {

  },


  exits: {
    success: {
      viewTemplatePath: 'pages/admin_register_requests',
      description: 'On sucess, redirect admin to `admin_register_requests` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function (inputs, exits) {

    // get request to retrieve registration requests from api with admin auth token
    request.get('https://mbtb-users.herokuapp.com/list_new_users/', {
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
