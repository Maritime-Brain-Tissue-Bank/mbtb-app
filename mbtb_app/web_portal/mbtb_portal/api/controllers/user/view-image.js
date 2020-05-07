const request = require('request');
const fs = require('fs');

module.exports = {


  friendlyName: 'View image',


  description: 'This controller receives filename from assets js and request and image from api and returns filename',


  inputs: {
    filename: {
      description: 'The id of the mbtb_data for detail view',
      type: 'string',
      required: true
    },

  },

  exits: {
  },


  fn: async function ({filename}, exits) {

    var req = this.req;

    // image url and payload
    let image_url = sails.config.custom.image_api_url + 'czi_image/';
    let payload = {
      filename : filename
    }

    // request to image api
    request.get({url: image_url, body: payload, json: true,
      'headers': {
        'content-type': 'application/json',
        'Authorization': 'Token ' + this.req.session.auth_token,
      }})
      .on('error', function (err) {
        console.log({
          'error_controller': 'user/view-image',
          'error_msg': err
        });
      })
      .pipe(fs.createWriteStream(sails.config.appPath + '/protected files/czi/' + filename + '.png'))

      // once writing file via writestream finish return value then to client
      .on('finish', function (response) {

        // for image access - to allow rendering image via this controller and image viewer, not via browser
        req.session.filename = filename;
        req.session.file_access = true;

        let file_url = '/images/czi/' + encodeURIComponent(filename) + '?';
        return exits.success({file_url: file_url, statusCode: 200});
      });

  },



};
