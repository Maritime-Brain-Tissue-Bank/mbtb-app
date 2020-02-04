module.exports = {


  friendlyName: 'Admin - View Data Guide',


  description: '',


  inputs: {

  },


  exits: {
    success:{
      viewTemplatePath: 'pages/view_data_guide',
      description: 'return view for displaying view data guide',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function (inputs, exits) {

    return exits.success();

  }


};
