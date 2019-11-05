module.exports = {


  friendlyName: 'Send template email',


  description: 'Send an email using a template.',


  inputs: {

    template:{
      description: 'The relative path to an html.ejs template within our `views/emails/` folder',
      example: 'email-reset-password',
      type: 'string',
      required: true
    },

    templateData:{
      description: 'A dictionary of data which will be accessible in the EJS template.',
      type: {},
      defaultsTo: {}
    },

    to:{
      description: 'The email address of the primary recipient.',
      example: 'foo@bar.com',
      required: true
    },

    subject: {
      description: 'The subject of the email.',
      example: 'Hello there.',
      defaultsTo: ''
    },

  },


  exits: {

    success: {

    }

  },


  fn: async function (inputs, exits) {

    sails.hooks.email.send(inputs.template, inputs.templateData, {
      to:inputs.to,
      subject: inputs.subject
      },
      function(err) {console.log(err || "Email sent from template");});

    return exits.success("Success");

  }


};

