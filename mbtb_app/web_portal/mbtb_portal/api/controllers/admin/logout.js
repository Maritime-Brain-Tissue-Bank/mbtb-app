module.exports = {


  friendlyName: 'Logout',


  description: 'Admin Logout action',


  inputs: {

  },


  exits: {

  },

  fn: async function (inputs, exits) {
    var res = this.res;

    // deleting session variables: admin_user, auth token
    // redirect a user to admin homepage
    delete this.req.session.admin_user;
    delete this.req.session.admin_auth_token_val;
    return res.redirect('/admin');
  }

};
