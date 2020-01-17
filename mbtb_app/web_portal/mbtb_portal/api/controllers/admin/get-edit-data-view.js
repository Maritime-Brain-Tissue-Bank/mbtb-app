const request = require('request');

module.exports = {


  friendlyName: 'Get edit data view',


  description: '',


  inputs: {
    id: {
      description: 'The id of the mbtb_data for detail view',
      type: 'number',
      required: true
    }
  },


  exits: {
    success: {
      viewTemplatePath: 'pages/admin_edit_data',
      description: 'On success, redirect admin to `admin_edit_data` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    },
    error_view: {
      viewTemplatePath: 'pages/message',
      description: 'return view to display msg',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function ({id}, exits) {

    const sex = ['Male', 'Female'];
    const preservation_method = ['Formalin-Fixed', 'Fresh Frozen', 'Both'];
    let neuropathology_diagnosis = null;
    let autopsy_type = null;
    let tissue_type = null;

    // urls for select options and data api
    let select_options_url = sails.config.custom.data_api_url + 'get_select_options/';
    let data_url = sails.config.custom.data_api_url + 'other_details/' + id + '/';

    // GET request for fetching select options
    request.get(select_options_url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err}); // log error to server console
          return exits.error_view({
            'msg_title': 'Error', 'msg_body': 'Something went wrong, please try again'
          });
        }
        else {
          const select_options_response = JSON.parse(body);
          neuropathology_diagnosis = select_options_response.neuropathology_diagnosis;
          autopsy_type = select_options_response.autopsy_type;
          tissue_type = select_options_response.tissue_type;
        }
      });


    // GET request for fetching data: single record
    request.get(data_url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
        }},
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err}); // log error to server console
        }
        else {
          var response = JSON.parse(body);

          // converting to int from str for displaying in number form fields
          response.age = parseInt(response.age);
          response.postmortem_interval = parseInt(response.postmortem_interval);
          response.time_in_fix = parseInt(response.time_in_fix);

          // return retrieved data to template in form of dictionary with key: `detailed_data`
          return exits.success({
            sex: sex, neuropathology_diagnosis: neuropathology_diagnosis, autopsy_type: autopsy_type,
            tissue_type:tissue_type, preservation_method: preservation_method, detailed_data: response
          });
        }
      });

  }


};
