const request = require('request');

module.exports = {

  friendlyName: 'New Account Request',

  description: 'New User - Request for a new account',

  inputs: {
    title: {
      type: 'string',
      required: false
    },

    first_name: {
      type: 'string',
      required: true
    },

    middle_name: {
      type: 'string',
      required: false
    },

    last_name: {
      type: 'string',
      required: true
    },

    email: {
      type: 'string',
      required: true
    },

    institution: {
      type: 'string',
      required: true
    },

    department_name: {
      type: 'string',
      required: true
    },

    current_position: {
      type: 'string',
      required: true
    },

    st_address_line_1: {
      type: 'string',
      required: false
    },

    st_address_line_2: {
      type: 'string',
      required: false
    },

    city: {
      type: 'string',
      required: true
    },

    province: {
      type: 'string',
      required: true
    },

    country: {
      type: 'string',
      required: true
    },

    postal_code: {
      type: 'string',
      required: false
    },

    comments: {
      type: 'string',
      required: false
    },

  },
  exits: {
    success: {
      viewTemplatePath: 'pages/message',
    },


  },


  fn: function (inputs, exits) {

    let data = {
      title: inputs.title,
      first_name: inputs.first_name,
      middle_name: inputs.middle_name,
      last_name: inputs.last_name,
      email: inputs.email,
      institution: inputs.institution,
      department_name: inputs.department_name,
      position_title: inputs.current_position,
      st_address_line_1: inputs.st_address_line_1,
      st_address_line_2: inputs.st_address_line_2,
      city: inputs.city,
      province: inputs.province,
      country: inputs.country,
      postal_code: inputs.postal_code,
      comments: inputs.comments,
    };

    request.post({url: 'http://127.0.0.1:8000/add_new_users/', formData: data},
      function optionalCallback(err, httpResponse, body) {
        var message_title = "";
        var message_body = "";

        if (err && httpResponse.statusCode !== 200) {
          message_title = "Error";
          message_body = err;
          return exits.success({msg_title: message_title, msg_body: message_body});
        }
        else if (httpResponse.statusCode === 400){
          message_title = "Error";
          message_body = "Invalid inputs or User with this email already exists";
          return exits.success({msg_title: message_title, msg_body: message_body});
        }
        else {
          message_title = "Confirmation";
          message_body = "Your request is received, it will take us 5 to 7 working days to process your request. ";
          return exits.success({msg_title: message_title, msg_body: message_body});
        }
      });
  }
};
