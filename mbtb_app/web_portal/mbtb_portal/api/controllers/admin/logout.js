module.exports = {


  friendlyName: 'Logout',


  description: 'Admin Logout',


  inputs: {

  },


  exits: {

  },

  fn: async function (inputs, exits) {
    var res = this.res;

    delete this.req.session.user_type;
    delete this.req.session.admin_auth_token_val;
    return res.redirect('/admin');
  }

};
