module.exports = {


  friendlyName: 'Admin - Get file upload view',


  description: 'This controller is to displaying admin_file_upload ejs template',


  inputs: {

  },


  exits: {
    success:{
      viewTemplatePath: 'pages/admin_file_upload',
      description: 'return view for displaying under construction msg',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function (inputs, exits) {

    return exits.success();

  }


};
