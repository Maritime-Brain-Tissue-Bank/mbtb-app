module.exports = {


  friendlyName: 'Get tissue requests terms',


  description: 'It redirects users to tissue requests terms page',


  inputs: {

  },


  exits: {
    success:{
      responseType: 'view',
      viewTemplatePath: 'pages/tissue_requests_terms',
      description: 'return view for displaying under construction msg'
    }
  },


  fn: async function (inputs, exits) {

    return exits.success();

  }


};
