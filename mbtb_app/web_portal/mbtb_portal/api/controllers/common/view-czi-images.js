module.exports = {


  friendlyName: 'View czi images',


  description: 'Display under construction page for "Czi images".',


  exits: {

    admin_response: {
      viewTemplatePath: 'pages/admin_message_response',
      description: 'For admin: on sucess, return to `admin_message_response` template',
      locals: {
        layout: 'layouts/admin_layout'
      }
    },

    user_response: {
      viewTemplatePath: 'pages/message',
      description: 'For users: on sucess, return to `message` template',
    }

  },


  fn: async function (inputs, exits) {
    let msg_title = "View Image"
    let msg_body = "This part is under construction at the moment, You'll find a tissue image soon.";

    if (this.req.session.admin_user) {
      return exits.admin_response({'msg_title': msg_title, 'msg_body': msg_body});
    }

    return exits.user_response({'msg_title': msg_title, 'msg_body': msg_body});
  }



};
