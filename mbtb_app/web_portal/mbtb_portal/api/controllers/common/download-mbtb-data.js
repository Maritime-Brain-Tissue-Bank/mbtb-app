const request = require('request');

module.exports = {


  friendlyName: 'Download mbtb data',


  description: 'Returning mbtb data in json format for admin & user.',


  inputs: {

    input_mbtb_codes: {
      type: 'json',
      required: false,
      description: 'Receives selected mbtb_codes from users for post request'
    },

    download_mode:{
      type: 'string',
      required: true,
      description: 'indicate what to download i.e. all data or filtered ones.'
    }
  },


  exits: {

  },


  fn: async function (inputs, exits) {

    let req = this.req;
    let res = this.res;
    let url = sails.config.custom.data_api_url + 'download_data/';
    let input_mbtb_codes = inputs.input_mbtb_codes;
    let download_mode = inputs.download_mode;
    let payload = [];
    let token_value = null;


    // Validating user or admin and fetching token value. If none, redirecting to 'logout'.
    if (req.session.admin_user){
      token_value = req.session.admin_auth_token_val;
    }

    else if (req.session.user_type === 'user'){
      token_value = req.session.auth_token
    }
    else {
      res.redirect('/logout');
    }


    // Prepare payload: whether to download all data or filtered ones
    if (download_mode === 'all'){
      payload = {
        download_mode: download_mode
      };
    }
    else {
      payload = {
        download_mode: download_mode,
        download_data: input_mbtb_codes
      };
    }


    // POST request to api for fetching the data
    request.post({
        url: url,
        body: payload,
        json: true,
        'headers': {
          'content-type': 'application/json',
          'Authorization': 'Token ' + token_value,
        }
      },
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({
            'error_controller': 'common/download-mbtb-data',
            'error_msg': err
          }); // log error to server console
          return exits.error_response({'msg_title': 'Error', 'msg_body': sails.config.custom.api_down_error_msg});
        }
        else {
          return exits.success({data: body, operation: "completed"});
        }
      }


    );


  },


};
