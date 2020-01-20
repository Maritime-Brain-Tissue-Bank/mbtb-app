const request = require('request');

module.exports = {


  friendlyName: 'Delete data',


  description: 'This controller perform delete request to api',


  inputs: {
    id: {
      description: 'The id of the mbtb_data for detail view',
      type: 'number',
      required: true
    },
  },


  exits: {

  },


  fn: async function ({id}, exits) {

    // url for API
    let url = sails.config.custom.data_api_url + 'delete_data/' + id + '/';

    // delete request to remove data along with admin auth token
    request.delete({url: url,
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
        }
      },
      function optionalCallback(err, httpResponse, body) {
        if (err && httpResponse.statusCode !== 200) {
          return exits.success("Error"); // return error response if something does wrong
        }
        else {
          return exits.success("Success");
        }
      });

  }

};
