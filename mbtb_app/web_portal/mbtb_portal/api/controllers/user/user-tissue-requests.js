module.exports = {


  friendlyName: 'User tissue requests',


  description: 'It redirects users to message page',


  inputs: {

  },


  exits: {
    success:{
      responseType: 'view',
      viewTemplatePath: 'pages/tissue_request_terms',
      description: 'return view for displaying under construction msg'
    }
  },


  fn: async function (inputs, exits) {

    return exits.success();

  }


};
