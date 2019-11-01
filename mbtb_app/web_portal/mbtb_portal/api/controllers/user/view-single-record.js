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
    var url = 'http://127.0.0.1:9000/other_details/' + id + '/'
    request.get(url, {
        'headers': {
          'Authorization': 'Token ' + sails.config.token.token_value,
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
