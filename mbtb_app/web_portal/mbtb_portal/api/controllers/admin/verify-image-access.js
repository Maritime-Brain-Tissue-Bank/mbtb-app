const fs = require('fs');
const path = require('path');

module.exports = {


  friendlyName: 'verify-image-access',


  description: 'This controller verify image access and render down the image to photo viewer js',


  inputs: {

  },


  exits: {

  },


  fn: async function (inputs, exits) {

    // ToDo: need a logic to authorize user here - maybe write a policy here

    var req = this.req;
    var res = this.res;

    let filename = req.param('filename');

    // Get the file path of the file on disk
    var filePath = path.resolve(sails.config.appPath, 'protected files', 'czi', filename + '.png');

    // ToDo: Should check that it exists here, but for demo purposes, assume it does
    // pipe a read stream to the response.
    fs.createReadStream(filePath).pipe(res);

  }


};
