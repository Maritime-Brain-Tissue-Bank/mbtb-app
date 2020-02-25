module.exports = {


  friendlyName: 'Data uploading guide',


  description: '',


  inputs: {

  },


  exits: {
    success:{
      viewTemplatePath: 'pages/admin_data_uploading_guide',
      description: 'return view for displaying data uploading guide',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function (inputs, exits) {

    return exits.success();

  }


};
