/**
 * Route Mappings
 * (sails.config.routes)
 *
 * Your routes tell Sails what to do each time it receives a request.
 *
 * For more information on configuring custom routes, check out:
 * https://sailsjs.com/anatomy/config/routes-js
 */

module.exports.routes = {

  /***************************************************************************
  *                                                                          *
  * Make the view located at `views/homepage.ejs` your home page.            *
  *                                                                          *
  * (Alternatively, remove this and add an `index.html` file in your         *
  * `assets` directory)                                                      *
  *                                                                          *
  ***************************************************************************/
  // users views
  'GET /':  { view: 'pages/homepage' },
  'GET /register':  { view: 'pages/user_registration' },
  'GET /login':  { view: 'pages/user_login' },
  'GET /policy': {view: 'pages/data_policy'},
  'GET /terms': {view: 'pages/terms'},
  'GET /faq': {view: 'pages/faq'},

  // admin views
  'GET /admin': {
    view: 'pages/admin_homepage',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },
  'GET /admin_login': {
    view: 'pages/admin_login',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },
  'GET /view_new_requests': {
    view: 'pages/admin_register_requests',
    locals: {
      layout: 'layouts/admin_layout'
    }
  }



  /***************************************************************************
  *                                                                          *
  * More custom routes here...                                               *
  * (See https://sailsjs.com/config/routes for examples.)                    *
  *                                                                          *
  * If a request to a URL doesn't match any of the routes in this file, it   *
  * is matched against "shadow routes" (e.g. blueprint routes).  If it does  *
  * not match any of those, it is matched against static assets.             *
  *                                                                          *
  ***************************************************************************/


};
