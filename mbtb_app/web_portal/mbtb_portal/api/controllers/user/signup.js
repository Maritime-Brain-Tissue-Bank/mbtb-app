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

  },


  fn: function (inputs, exits) {

    let data = {
      position_title: inputs.title,
      first_name: inputs.first_name,
      middle_name: inputs.middle_name,
      last_name: inputs.last_name,
      email: inputs.email,
      institution: inputs.institution,
      department_name: inputs.department_name,
      current_position: inputs.current_position,
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
        if (err && httpResponse.statusCode !== 200) {
          return exits.success(err);
        }
        else if (httpResponse.statusCode === 400){
          return exits.success("Invalid inputs or User with this email already exists")
        }
        else {
          return exits.success("Your request is received, it will take us 5 to 7 working days to process your request. ")
        }
      });
  }
};
