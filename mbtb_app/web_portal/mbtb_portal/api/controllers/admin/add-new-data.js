const request = require('request');

module.exports = {


  friendlyName: 'Add new data',


  description: `It redirects to the "admin_add_new_data" template and load data for dropdowns i.e. autopsy_type, tissue_type
                , storage_methods, sex, disease_names`,


  inputs: {

  },


  exits: {
    success: {
      viewTemplatePath: 'pages/admin_add_new_data',
      locals: {
        layout: 'layouts/admin_layout'
      }
    },

    error_view: {
      responseType: 'view',
      viewTemplatePath: 'pages/message',
      description: 'return view to display msg'
    }
  },


  fn: async function (inputs, exits) {

    const sex = ['Male', 'Female'];
    const storage_methods = ['Formalin-Fixed', 'Fresh Frozen', 'Both'];

    let url = sails.config.custom.data_api_url + 'get_select_options/';

    // get request to retrieve registration requests from api with admin auth token
    request.get(url, {
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
          const response = JSON.parse(body);
          return exits.success({
            sex: sex, neuro_diagnosis: response.neuoropathology_diagnosis, autopsy_type:response.autopsy_type,
            tissue_type:response.tissue_type, storage_method: storage_methods
          });
        }
      });


  }


};
