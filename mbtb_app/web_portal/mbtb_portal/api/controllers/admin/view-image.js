module.exports = {


  friendlyName: 'View image',


  description: 'Display "Image" page.',

  inputs: {
    filename: {
      description: 'The id of the mbtb_data for detail view',
      type: 'string',
      required: false
    },

  },

  exits: {

    success: {
      viewTemplatePath: 'pages/admin_view_image',
      description: 'On sucess, return to `view_single_record` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    },


  },


  fn: async function (inputs, exits) {

    var req = this.req;
    let filename = req.param("filename");
    let dir = "/images/" + encodeURIComponent(filename) + ".png";
    let tissue_details = filename.split(" ");



    return exits.success({image_url: dir,
                          tissue_name: tissue_details[0].slice(1),
                          region_name: tissue_details[1].slice(1),
                          stain_name: tissue_details[2].slice(1)
    });



  },


};
