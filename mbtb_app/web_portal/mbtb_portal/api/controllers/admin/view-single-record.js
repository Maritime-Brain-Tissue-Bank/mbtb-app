const request = require('request');

module.exports = {


  friendlyName: 'View single record',


  description: 'Retrieve detailed mbtb data from api i.e. for a single request',


  inputs: {

    id: {
      description: 'The id of the mbtb_data for detail view',
      type: 'number',
      required: true
    },

  },


  exits: {

    success: {
      viewTemplatePath: 'pages/view_single_record',
      description: 'On sucess, return to `view_single_record` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }

  },


  fn: async function ({id}, exits) {

    // get request to retrieve detailed mbtb data for single id from api with admin auth token
    var url = 'https://mbtb-data.herokuapp.com/other_details/' + id + '/';
    request.get(url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err}); // log error to server console
        }
        else {
          var response = JSON.parse(body);

          // return retrieved data to template in form of dictionary with key: `detailed_data`
          return exits.success({detailed_data: response});
        }
      });


  }


};
