module.exports = {


  friendlyName: 'Logout',


  description: 'Admin Logout',


  inputs: {

  },


  exits: {
    success: {
      viewTemplatePath: 'pages/admin_homepage',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },

  fn: async function (inputs, exits) {

    sails.config.token.update_role = '';
    sails.config.token.update_token_value = null;
    return exits.success();
  }

};
