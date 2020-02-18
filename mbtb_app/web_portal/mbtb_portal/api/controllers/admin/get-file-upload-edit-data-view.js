module.exports = {


  friendlyName: 'Admin - Get file upload view',


  description: 'This controller is to displaying admin_file_upload ejs template for edit data via file',


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
    let data_mode = 'Edit Data';
    let url = 'edit_file_upload/';
    return exits.success({data_mode: data_mode, url: url});

  }


};
