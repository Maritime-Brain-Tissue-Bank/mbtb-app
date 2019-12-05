const request = require('request');

module.exports = {


  friendlyName: 'View data table',


  description: 'Retrieve mbtb data from API',


  inputs: {

  },


  exits: {

    success: {
      viewTemplatePath: 'pages/admin_view_data_table',
      description: 'On sucess, return to `admin_view_data_table` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }

  },


  fn: async function (inputs, exits) {
    let url = sails.config.custom.data_api_url + 'brain_dataset/';

    let clinical_diagnosis = [];
    let neuropathology_diagnosis = [];
    let tissue_type = [];
    let preservation_method = [];

    // get request to retrieve mbtb data from api with admin auth token
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

          // To Do: rewrite below logic (storage year, select options unique values) in API, for now written to save API calls

          // splitting storage_year and discarding time
          for (var i=0; i < response.length; i++){
            var time_date = response[i].storage_year.split("T");
            response[i].storage_year = time_date[0];
          }

          // Function: for finding unique values, for dro-down lists
          function get_values(parameter_name) {
            let local_array = [];

            // for finding unique elemenets in array
            let unique = (value, index, self) => {
              return self.indexOf(value) === index
            };

            for (item=0; item < response.length; item++){
              if (response[item][parameter_name] !== ''){
                local_array.push(response[item][parameter_name]);
              }
            }

            local_array = local_array.filter(unique);
            return local_array;
          }

          // filtering unique items
          clinical_diagnosis = get_values('clinical_diagnosis');
          neuropathology_diagnosis = get_values('neuro_diagnosis_id');
          tissue_type = get_values('tissue_type');
          preservation_method = get_values('preservation_method');

          // return retrieved data to template in form of dictionary with key: `data`
          return exits.success({
            data: response, clinical_diagnosis: clinical_diagnosis, neuropathology_diagnosis: neuropathology_diagnosis,
            tissue_type: tissue_type, preservation_method: preservation_method
          });
        }
      });
  }


};
