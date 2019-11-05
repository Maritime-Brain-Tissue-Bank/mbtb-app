module.exports = function authorized() {

  var req = this.req;
  var res = this.res;

  if (req.wantsJSON) {
    return res.sendStatus(401);
  }

  else {

    if (sails.config.token.token_value) {
      return res.redirect('/admin');
    }
  }

};
