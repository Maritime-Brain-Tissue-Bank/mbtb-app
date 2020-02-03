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
  'GET /view_data': { action: 'user/view-data-table' },
  'GET /logout': { action: 'user/logout'},
  'GET /view_data/:id': {action: 'user/view-single-record'},
  'GET /tissue_requests': {action: 'user/user-tissue-requests'},

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

  'POST /approve_user_requests': {
    action: 'admin/approve-user-requests',
  },

  'POST /deny_user_requests': {
    action: 'admin/deny-user-requests',
  },

  'GET /admin_view_data': {
    action: 'admin/view-data-table',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /admin_view_data/:id': {
    action: 'admin/view-single-record',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /insert_single_row': {
    action: 'admin/insert-single-row-data',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /file_upload': {
    action: 'admin/get-file-upload-add-data-view',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /file_upload': {
    action: 'admin/file-upload-add-data',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /edit_data/:id': {
    action: 'admin/get-edit-data-view',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /edit_data/': {
    action: 'admin/edit-data',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'DELETE /delete_data/:id': {
    action: 'admin/delete-data',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /data_uploading_guide': {
    action: 'admin/data-uploading-guide',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /edit_file_upload': {
    action: 'admin/get-file-upload-edit-data-view',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /edit_file_upload': {
    action: 'admin/file-upload-edit-data',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

};
