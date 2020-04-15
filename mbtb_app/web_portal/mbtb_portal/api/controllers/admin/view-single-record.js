const request = require('request-promise');

// async function: get request with promise using `request-promise` return json response
async function getRequestData(url, token) {
  return request.get({
    uri: url,
    headers: {
      Authorization: 'Token ' + token,
    },
    json: true,
    simple: false,
    resolveWithFullResponse: true

  }).then(res => ({
    statusCode: res.statusCode,
    data: res.body
  }
    )
  ).catch(function (err) {
    console.log("************************************\n")
    console.log("Controller: admin/view-single-record\n");
    console.log(err);
    });
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

    // call to function and await for the response
    text_data = await getRequestData(text_data_url, this.req.session.admin_auth_token_val);
    meta_data = await getRequestData(meta_data_url, this.req.session.admin_auth_token_val);

    // error validation return error msg in case of error from api i.e. 404, 500
    if (text_data.statusCode != 200){
      // ToDo: need to redict to ejs view to display message i.e. data not found.
    }

    if (meta_data.statusCode != 200) {
      meta_data.data = meta_data.data["Error"];
    }

    return {detailed_data: text_data.data, tissue_meta_data: meta_data.data};

  },


};
