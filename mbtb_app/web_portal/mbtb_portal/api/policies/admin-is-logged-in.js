module.exports = async function (req, res, proceed) {

  if (req.session.admin_auth_token_val && req.session.admin_user === true) {
    return proceed();
  }

  if (req.session.auth_token || req.session.user_type === 'user'){
    try {
      delete req.session.user_type;
      delete req.session.auth_token;
      return res.redirect('/');
    }
    catch (e) {
      return res.redirect('/');
    }
  }
  //--•
  // Otherwise, this request did not come from a logged-in user.
  return res.redirect('/admin_login');

};
