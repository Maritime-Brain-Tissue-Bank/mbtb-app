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
  'GET /view_data_guide': {action: 'user/view-data-guide'},
  'GET /tissue_requests_terms': {action: 'user/tissue-requests-terms'},
  'GET /tissue_requests_form': { action: 'user/get-tissue-requests-form'},
  'POST /tissue_requests_form': { action: 'user/tissue-requests-form'},
  'GET /get_image': { action: 'user/view-image'},
  'GET /images/czi/:filename?': { action: 'user/verify-image-access'},

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

  'GET /admin_view_data_guide': {
    action: 'admin/view-data-guide',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /get_new_tissue_requests': {
    action: 'admin/get-tissue-requests',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /get_archive_tissue_requests': {
    action: 'admin/get-archive-tissue-requests',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /approve_tissue_requests': {
    action: 'admin/approve-tissue-requests',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /revert_archive_tissue_requests': {
    action: 'admin/revert-archive-tissue-requests',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /view_single_tissue_request/:id': {
    action: 'admin/view-single-tissue-request',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /view_single_archive_tissue_request/:id': {
    action: 'admin/view-single-archive-tissue-request',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /delete_tissue_requests': {
    action: 'admin/delete-tissue-requests',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /delete_archive_tissue_requests': {
    action: 'admin/delete-archive-tissue-requests',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /download_data': {
    action: 'common/download-mbtb-data',
  },

  'GET /view_current_users': {
    action: 'admin/current-users',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /view_suspended_users': {
    action: 'admin/suspended-users',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /view_current_users/:id': {
    action: 'admin/view-single-current-user',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'GET /view_suspended_users/:id': {
    action: 'admin/view-single-suspended-user',
    locals: {
      layout: 'layouts/admin_layout'
    }
  },

  'POST /suspend_user_form':{
    action:'admin/suspend-user-form',
    locals:{
      layout:'layouts/admin_layout'
    }
  },

  'POST /suspend_user_with_reason':{
    action:'admin/suspend-user-with-reason',
    locals:{
      layout:'layouts/admin_layout'
    }
  },

  'POST /revert_user_form':{
    action:'admin/revert-user-form',
    locals:{
      layout:'layouts/admin_layout'
    }
  },

  'POST /revert_user_with_reason':{
    action:'admin/revert-user-with-reason',
    locals:{
      layout:'layouts/admin_layout'
    }
  },

  'GET /admin_get_image': {
    action: 'admin/view-image',
    locals:{
      layout:'layouts/admin_layout'
    }
  },

  'GET /admin_images/czi/:filename?': {
    action: 'admin/verify-image-access',
    locals:{
      layout:'layouts/admin_layout'
    }
  },

};
