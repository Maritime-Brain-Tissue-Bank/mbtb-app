module.exports = {


  friendlyName: 'Revert user form',


  description: 'Display revert user form',


  inputs: {
    requests_ids:{
      type: 'json',
      required: true,
      description: 'Receives selected ids from admin for patch request'
    }

  },


  exits: {
    success:{
      viewTemplatePath: 'pages/revert_user_form',
      description: 'return view for reverting suspended user with reason',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },

  fn: async function (inputs, exits) {

    console.log("\n\n  **************   \n\n");
    console.log(inputs.requests_ids + " :inside controller \n");

    return exits.success({requests_ids: inputs.requests_ids});

  }


};
