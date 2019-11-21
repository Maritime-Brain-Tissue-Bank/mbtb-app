module.exports = {


  friendlyName: 'User tissue requests',


  description: 'It redirects users to message page',


  inputs: {

  },


  exits: {
    success:{
      responseType: 'view',
      viewTemplatePath: 'pages/message',
      description: 'return view for displaying under construction msg'
    }
  },


  fn: async function (inputs, exits) {
    let msg_title = 'Tissue Requests';
    let msg_body = 'This feature is coming soon!';

    return exits.success({msg_title: msg_title, msg_body: msg_body});

  }


};
