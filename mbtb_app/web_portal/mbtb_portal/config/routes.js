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
  'POST /register': { action: 'user/signup' },
  'GET /login':  { view: 'pages/user_login' },
  'POST /login': { action: 'user/login' },
  'GET /policy': { view: 'pages/data_policy' },
  'GET /terms': { view: 'pages/terms' },
  'GET /faq': { view: 'pages/faq' },
  'GET /view_data_table': { action: 'user/view-data-table' },
  'GET /logout': { action: 'user/logout'},

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

  'POST /admin_login': {
    action: 'admin/login',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /view_new_requests':{
    action: 'admin/register-requests',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /add_new_data': {
    action: 'admin/add-new-data',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /admin_logout': {
    action: 'admin/logout',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /admin_faq': {
    view: 'pages/admin_faq',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /admin_policy': {
    view: 'pages/data_policy',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /admin_terms': {
    view: 'pages/terms',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

};
