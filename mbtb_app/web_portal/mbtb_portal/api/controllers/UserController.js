/**
 * UserController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */
const request = require('request');

module.exports = {

  login: function (req, res) {
    let credentials = {
        email: req.param('user_email'),
        password: req.param('user_password'),
      };

    request.post({url:'http://127.0.0.1:8000/user_auth', formData: credentials},
      function optionalCallback(err, httpResponse, body) {
      if (err && httpResponse.statusCode !== 200) {
        console.error('User Login Response:', err);
        return res.error(err);
      }
      else {
        console.log('User Login Response: ', body);
        return res.ok(body);
      }
    });
  }
};
