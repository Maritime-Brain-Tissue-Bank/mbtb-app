module.exports = {


  friendlyName: 'Logout',


  description: 'Admin Logout',


  inputs: {

  },


  exits: {

  },

  fn: async function (inputs, exits) {
    var res = this.res;

    sails.config.token.update_role = '';
    sails.config.token.update_token_value = null;
    return res.redirect('/admin');
  }

};
