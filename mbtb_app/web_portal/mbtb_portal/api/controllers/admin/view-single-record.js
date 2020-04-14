const request = require('request');
var EventEmitter = require('events');

module.exports = {


  friendlyName: 'View single record',


  description: 'Retrieve detailed mbtb data from api i.e. for a single request',


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


  fn: async function ({id}, exits) {

    // ToDo: write a logic to fetch meta data from image api, below is sample data
    let tissue_meta_data = {
      "one_region":[
        {
          "stain_name": "one - 111",
          "file_name": "#bb00-002 #1 #1.czi"
        },{
          "stain_name": "one - 222",
          "file_name": "#bb00-002 #1 #2.czi"
        }
      ],
      "second_region":[
        {
          "stain_name": "sec - 999",
          "file_name": "#bb00-002 #1 #1.czi"
        },{
          "stain_name": "sec - 888",
          "file_name": "#bb00-002 #1 #2.czi"
        }
      ]
    };

    var tissue_text_data = new EventEmitter();

    // get request to retrieve detailed mbtb data for single id from api with admin auth token
    let url = sails.config.custom.data_api_url + 'other_details/' + id + '/';
    request.get(url, {
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
        }
      },
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err}); // log error to server console
        } else {
          tissue_text_data.data = JSON.parse(body);
          tissue_text_data.emit('update');
        }
      });

    // waiting for tissue_text_data' state change to update
    tissue_text_data.on('update', function () {

      // return retrieved data to template in form of dictionary with key: `detailed_data`
      return exits.success({detailed_data: tissue_text_data.data,
                            tissue_meta_data: tissue_meta_data
      });
    })

  }


};
