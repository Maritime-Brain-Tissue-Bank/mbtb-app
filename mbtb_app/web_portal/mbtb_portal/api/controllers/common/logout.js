module.exports = {


  friendlyName: 'Logout',


  description: 'User Logout',


  inputs: {

  },


  exits: {
    success: {
      viewTemplatePath: 'pages/homepage',
    }
  },


  fn: async function (inputs, exits) {
    sails.config.token.update_role = '';
    sails.config.token.update_token_value = null;
    return exits.success();

  }


};
