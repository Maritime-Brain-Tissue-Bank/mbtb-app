const request = require('request');
const fs = require('fs');

module.exports = {

  friendlyName: 'Admin - File upload',


  description: 'This controller upload file to sails js and send it via PATCH request to API for edit data',


  inputs: {

  },


  exits: {
    return_view: {
      responseType: 'view',
      viewTemplatePath: 'pages/admin_message_response',
      description: 'return view to display msg'
    }
  },


  fn: async function (inputs, exits) {

    let req = this.req;
    let res = this.res;

    let url = sails.config.custom.data_api_url + 'file_upload/';
    let upload_file = req.file('upload_file'); // getting file from request
    let temp_file_dir = '';

    // Uploading file to sails first
    upload_file.upload({
        maxBytes : 500000000}, // file upload size limit 500 MB
      function onUploadComplete(err, files) {

        // Files will be uploaded to .tmp/uploads
        if (err) {
          return res.serverError(err);  // IF ERROR Return and send 500 error with error
        }
        temp_file_dir = files[0].fd; // temporary file path

        request.patch({
            url: url,
            formData: {
              'file': fs.createReadStream(temp_file_dir)
            },
            'headers': {
              'Authorization': 'Token ' + req.session.admin_auth_token_val,
              'Content-Type': 'multipart/form-data'
            }
          },
          function optionalCallback(err, httpResponse, body) {
            fs.unlink(temp_file_dir, function(file_error) { // removing uploaded file to sails
              if (file_error) return console.log(err); // log error related to deleting file

              if (err) {
                console.log(err); // log error to server console related to post request
              }
              else {

                try {
                  const response = JSON.parse(body);

                  if(response.Error){
                    // for displaying validation data validation error
                    if (response.Message === undefined){
                      msg = JSON.stringify(response.Error);
                      return exits.return_view({'msg_title': 'Error', 'msg_body': msg}) // display error msg
                    }

                    // for displaying column names error
                    msg = response.Message + ' with following reason: ' + JSON.stringify(response.Error);
                    return exits.return_view({'msg_title': 'Error', 'msg_body': msg}) // display error msg
                  }

                  // for displaying successful response
                  else if (response.Response){
                    let view_data_url = 'admin_view_data/' ;
                    msg = 'Cheers, Your data is updated.';
                    return exits.return_view({'msg_title': 'Confirmation', 'msg_body': msg, view_data_url: view_data_url});
                  }
                }

                catch (e) {
                  msg = 'Something went wrong, Please try again';
                  return exits.return_view({'msg_title': 'Error', 'msg_body': msg});
                }
              }

            });

          });

      });

  }

};
