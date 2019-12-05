module.exports = {


  friendlyName: 'Logout',


  description: 'User Logout',


  inputs: {

  },


  exits: {

  },

  fn: async function (inputs, exits) {
    var res = this.res;

    // deleting session variables: user_type, auth token
    // redirect a user to user homepage
    delete this.req.session.user_type;
    delete this.req.session.auth_token;

    return res.redirect('/');

  }

};
