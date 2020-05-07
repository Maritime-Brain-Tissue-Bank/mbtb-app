const fs = require('fs');
const path = require('path');

module.exports = {


  friendlyName: 'verify-image-access',


  description: 'This controller verify image access and render down the image to photo viewer js',


  inputs: {

  },


  exits: {
    not_authorized: {
      viewTemplatePath: 'pages/admin_message_response',
      description: 'return to this view when user try to access image directly.',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function (inputs, exits) {

    var req = this.req;
    var res = this.res;

    let filename = req.param('filename');

    // Get the file path of the file on disk
    let file_path = path.resolve(sails.config.appPath, 'protected files', 'czi', filename + '.png');

    if (req.session.admin_user && req.session.file_access && req.session.filename === filename){

      // remove filename and file_access session variables
      delete req.session.filename;
      delete req.session.file_access;

      // pipe a read stream to the response.
      fs.createReadStream(file_path).pipe(res);
    }
    else {

      // not authorized return view
      let msg_body = "You are not authorized to view this image directly.";
      return exits.not_authorized({'msg_title': "Authorization Error", 'msg_body': msg_body});

    }


  }


};
