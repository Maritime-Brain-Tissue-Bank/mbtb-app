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
    request.get('https://mbtb-users.herokuapp.com/list_new_users/', {
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
