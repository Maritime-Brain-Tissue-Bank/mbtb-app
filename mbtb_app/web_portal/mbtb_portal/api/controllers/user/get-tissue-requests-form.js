module.exports = {


  friendlyName: 'Get tissue requests form',


  description: 'This controller display tissue request form to the users',


  inputs: {

  },


  exits: {
    success:{
      responseType: 'view',
      viewTemplatePath: 'pages/tissue_requests_form',
      description: 'return view for displaying tissue request form'
    }
  },


  fn: async function (inputs, exits) {

    return exits.success();

  }


};
