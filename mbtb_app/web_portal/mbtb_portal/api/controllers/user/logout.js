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
    delete this.req.session.user_type;
    delete this.req.session.auth_token;

    return exits.success();

  }

};
