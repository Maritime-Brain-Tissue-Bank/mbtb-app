module.exports = {


  friendlyName: 'View data table',


  description: 'Display "Data table" page.',


  inputs: {

  },


  exits: {

    success: {
      viewTemplatePath: 'pages/view_data_table'
    }

  },


  fn: async function (inputs, exits) {

    // Respond with view.
    return exits.success();
  }




};
