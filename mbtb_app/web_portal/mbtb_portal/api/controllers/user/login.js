const request = require('request');

module.exports = {

  friendlyName: 'Welcome User',

  description: 'Look up the specified user and welcome them',

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

    bad_combo: {
      responseType: 'view',
      viewTemplatePath: 'pages/user_login',
      description: 'return view for password mismatch, display error msg'
    }
  },


  fn: function (inputs, exits) {
    var req = this.req;
    var res = this.res;

    let credentials = {
      email: inputs.user_email,
      password: inputs.user_password,
    };

    // post request for retrieving auth token from api, with credentials as payload
    request.post({url: 'https://mbtb-users.herokuapp.com/user_auth', formData: credentials},
      function optionalCallback(err, httpResponse, body) {
        if (err && httpResponse.statusCode !== 200) {
          return exits.success({'Error': err}); // display error msg if something goes wrong with request
        }
        else {
          try {
            const response = JSON.parse(body);
            if(typeof (response) == "object"){
              return exits.bad_combo({'error_msg': response.Error}) // display error msg for wrong email, password
            }
          }
          catch (e) {
            // set session variables: user_type to `user` and save auth token for further usage
            // redirect to user homepage
            req.session.user_type = 'user';
            req.session.auth_token = body;
            return res.redirect('/')
          }
        }
      });
  }
};
