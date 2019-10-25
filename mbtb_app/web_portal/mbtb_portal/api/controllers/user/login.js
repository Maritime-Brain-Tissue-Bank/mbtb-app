const request = require('request');

module.exports = {

  friendlyName: 'Welcome Admin',

  description: 'Look up the specified admin and welcome them',

  inputs: {
    user_email: {
      description: 'The email to try in this attempt, e.g. "irl@example.com".',
      type: 'string',
      required: true
    },

    user_password: {
      description: 'The unencrypted password to try in this attempt, e.g. "passwordlol".',
      type: 'string',
      required: true
    }
  },
  exits: {
    success: {
      viewTemplatePath: 'pages/homepage',
    },

    bad_combo: {
      responseType: 'view',
      viewTemplatePath: 'pages/user_login'
    }
  },


  fn: function (inputs, exits) {

    let credentials = {
      email: inputs.user_email,
      password: inputs.user_password,
    };

    request.post({url: 'http://127.0.0.1:8000/user_auth', formData: credentials},
      function optionalCallback(err, httpResponse, body) {
        if (err && httpResponse.statusCode !== 200) {
          return exits.success({'Error': err});
        }
        else {
          try {
            const response = JSON.parse(body);
            if(typeof (response) == "object"){
              return exits.bad_combo({'error_msg': response.Error})
            }
          }
          catch (e) {
            sails.config.token.name = 'user';
            sails.config.token.update_token_value = body;
            return exits.success();
          }
        }
      });
  }
};
