const request = require('request');

module.exports = {


  friendlyName: 'View data table',


  description: 'Display "Data table" page.',


  inputs: {

  },


  exits: {

    success:{
      viewTemplatePath: 'pages/view_data_table'
    },

  },


  fn: async function (inputs, exits) {
    request.get('http://127.0.0.1:9000/brain_dataset/', {
        'headers': {
          'Authorization': 'Token ' + sails.config.token.token_value,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err});
        }
        else {
          var response = JSON.parse(body);

          // splitting storage_year and discarding time
          for (var i=0; i < response.length; i++){
            var time_date = response[i].storage_year.split("T");
            response[i].storage_year = time_date[0];
          }
          return exits.success({data: response});
        }
      });
  }




};
