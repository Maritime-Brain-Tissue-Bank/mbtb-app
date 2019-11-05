const request = require('request');

module.exports = {


  friendlyName: 'View single record',


  description: 'Display "Single record" page.',


  inputs: {

    id: {
      description: 'The id of the mbtb_data for detail view',
      type: 'number',
      required: true
    },

  },


  exits: {

    success: {
      viewTemplatePath: 'pages/view_single_record'
    }

  },


  fn: async function ({id}, exits) {
    var url = 'https://mbtb-data.herokuapp.com/other_details/' + id + '/';
    request.get(url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.auth_token,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err});
        }
        else {
          var response = JSON.parse(body);

          return exits.success({detailed_data: response});
        }
      });


  }
};
