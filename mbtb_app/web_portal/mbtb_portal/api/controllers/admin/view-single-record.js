const request = require('request-promise');

// async function: get request with promise using `request-promise` return json response
async function getRequestData(url, token) {
  return request.get({
    uri: url,
    headers: {
      Authorization: 'Token ' + token,
    },
    json: true,
    resolveWithFullResponse: true

  }).then(res => (
    res.body
    )
  );
}

module.exports = {


  friendlyName: 'View single record',


  description: 'Retrieve detailed mbtb data and image meta data (regions, stains) from apis i.e. for a single request',


  inputs: {

    id: {
      description: 'The id of the mbtb_data for detail view',
      type: 'number',
      required: true
    },

  },


  exits: {

    success: {
      viewTemplatePath: 'pages/admin_view_single_record',
      description: 'On sucess, return to `view_single_record` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }

  },


  fn: async function ({id}) {

    // urls for api: for fetching text data and meta data for tissue
    let text_data_url = sails.config.custom.data_api_url + 'other_details/' + id + '/';
    let meta_data_url = sails.config.custom.image_api_url + 'tissue_meta_data/' + id + '/';
    let text_data, meta_data;

    try {

      // call to function and await for the response
      text_data = await getRequestData(text_data_url, this.req.session.admin_auth_token_val);
      meta_data = await getRequestData(meta_data_url, this.req.session.admin_auth_token_val);

      return {detailed_data: text_data, tissue_meta_data: meta_data};

    } catch (e) {

      console.log({'error_msg': e}); // log error to server console
      return {detailed_data: {}, tissue_meta_data: {}};
    }

  },


};
