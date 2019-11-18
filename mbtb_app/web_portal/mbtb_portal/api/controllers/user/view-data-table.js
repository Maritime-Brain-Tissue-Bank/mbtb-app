const request = require('request');

module.exports = {


  friendlyName: 'View data table',


  description: 'Retrieve mbtb data from API',


  inputs: {

  },


  exits: {

    success:{
      viewTemplatePath: 'pages/view_data_table',
      description: 'On sucess, return to `view_data_table` template',
    },

  },


  fn: async function (inputs, exits) {
    let url = sails.config.custom.data_api_url + 'brain_dataset/';

    // get request to retrieve mbtb data from api with user auth token
    request.get(url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.auth_token,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err}); // log error to server console
        }
        else {
          var response = JSON.parse(body);

          // splitting storage_year and discarding time
          for (var i=0; i < response.length; i++){
            var time_date = response[i].storage_year.split("T");
            response[i].storage_year = time_date[0];
          }
          // return retrieved data to template in form of dictionary with key: `data`
          return exits.success({data: response});
        }
      });
  }

};
