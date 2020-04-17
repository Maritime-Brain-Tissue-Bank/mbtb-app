module.exports = {


  friendlyName: 'Suspend user form',


  description: 'Display suspend user form',


  inputs: {
    requests_ids:{
      type: 'json',
      required: true,
      description: 'Receives selected ids from admin for patch request'
    }

  },


  exits: {
    success:{
      viewTemplatePath: 'pages/suspend_user_form',
      description: 'return view for suspending user reason',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },

  fn: async function (inputs, exits) {
    
    return exits.success({requests_ids: inputs.requests_ids});

  }


};
