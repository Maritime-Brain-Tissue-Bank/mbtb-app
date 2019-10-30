module.exports = async function (req, res, proceed) {

  if (sails.config.token.token_value) {
    return proceed();
  }

  //--•
  // Otherwise, this request did not come from a logged-in user.
  return res.redirect('/login');

};
