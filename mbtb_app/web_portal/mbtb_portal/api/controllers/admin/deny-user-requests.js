const request = require('request');

module.exports = {


  friendlyName: 'Deny user requests',


  description: 'Deny new account requests',


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

      request.delete({url: url,
          'headers': {
            'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
          }
        },
        function optionalCallback(err, httpResponse, body) {
          if (err && httpResponse.statusCode !== 200) {
            return exits.success("error");
          }
          else {
            console.log("New user request denied, ID: ", id);
          }
        });
    }
    return exits.success("completed");

  }


};
