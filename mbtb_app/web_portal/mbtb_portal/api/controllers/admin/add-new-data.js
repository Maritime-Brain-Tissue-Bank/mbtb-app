module.exports = {


  friendlyName: 'Add new data',


  description: '',


  inputs: {

  },


  exits: {
    success: {
      viewTemplatePath: 'pages/admin_add_new_data',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function (inputs, exits) {

    return exits.success();

  }


};
