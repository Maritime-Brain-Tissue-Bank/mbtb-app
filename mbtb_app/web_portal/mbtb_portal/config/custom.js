/**
 * Custom configuration
 * (sails.config.custom)
 *
 * One-off settings specific to your application.
 *
 * For more information on custom configuration, visit:
 * https://sailsjs.com/config/custom
 */

module.exports.custom = {

  /***************************************************************************
  *                                                                          *
  * Any other custom config this Sails app should use during development.    *
  *                                                                          *
  ***************************************************************************/
  // mailgunDomain: 'transactional-mail.example.com',
  // mailgunSecret: 'key-testkeyb183848139913858e8abd9a3',
  // stripeSecret: 'sk_test_Zzd814nldl91104qor5911gjald',
  // …

  baseUrl: 'http://localhost:1337',
  image_api_url: 'http://127.0.0.1:7000/',  // image api url
  user_api_url: 'http://127.0.0.1:8000/', // user api url i.e. for user, admin login, register
  data_api_url: 'http://127.0.0.1:9000/', // data api url
  api_down_error_msg: 'Servers are down, please contact site admin for the help.', // apis are down error message

};
