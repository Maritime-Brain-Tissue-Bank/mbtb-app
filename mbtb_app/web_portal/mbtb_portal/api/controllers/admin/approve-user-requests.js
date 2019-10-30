var generator = require('generate-password');
const request = require('request');

module.exports = {


  friendlyName: 'Approve user requests',


  description: '',


  inputs: {
    requests_ids:{
      type: 'json',
      required: true
    },
  },


  exits: {

  },


  fn: async function (inputs, exits) {
    var request_ids = inputs.requests_ids;

    for (id of request_ids){

      var url = 'http://127.0.0.1:8000/list_new_users/' + id + '/';
      let payload = {
        pending_approval: "N",
        password_hash: generator.generate({
          length: 15,
          numbers: true
        })
      };

      request.patch({url: url, body: payload, json: true,
          'headers': {
            'content-type': 'application/json',
            'Authorization': 'Token ' + sails.config.token.token_value,
          }
        },
        function optionalCallback(err, httpResponse, body) {
          if (err && httpResponse.statusCode !== 200) {
            return exits.success("error");
          }
          else {
            console.log("approved");
          }
        });
    }
    return exits.success("approved");
  }


};
