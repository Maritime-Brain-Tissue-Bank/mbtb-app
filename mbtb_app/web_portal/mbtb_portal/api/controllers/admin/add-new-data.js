module.exports = {


  friendlyName: 'Add new data',


  description: 'This controller is for adding a new data to DB. For now, it redirects to the "admin_add_new_data" template',


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
