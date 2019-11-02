const request = require('request');

module.exports = {


  friendlyName: 'Register requests',


  description: '',


  inputs: {

  },


  exits: {
    success: {
      viewTemplatePath: 'pages/admin_register_requests',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function (inputs, exits) {
    request.get('http://127.0.0.1:8000/list_new_users/', {
      'headers': {
        'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
      }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err});
        }
        else {
          const response = JSON.parse(body);
          return exits.success({data: response});
        }
      });

  }

};
