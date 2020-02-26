/**
 * Policy Mappings
 * (sails.config.policies)
 *
 * Policies are simple functions which run **before** your actions.
 *
 * For more information on configuring policies, check out:
 * https://sailsjs.com/docs/concepts/policies
 */

module.exports.policies = {

  /***************************************************************************
  *                                                                          *
  * Default policy for all controllers and actions, unless overridden.       *
  * (`true` allows public access)                                            *
  *                                                                          *
  ***************************************************************************/

  // admin side
  'admin/*': 'admin-is-logged-in',

  // Bypass the `is-logged-in` policy for:
  'admin/login': true,
  'admin/logout': true,

  // user side
  'user/*': 'user-is-logged-in',

  // Bypass the `is-logged-in` policy for:
  'user/login': true,
  'user/logout': true,
  'user/signup': true,

};
