const request = require('request');
const moment = require('moment');

module.exports = {


  friendlyName: 'Tissue requests form',


  description: 'This controller is to post tissue request data to the data api',


  inputs: {
    title: {
      type: 'string',
      required: false
    },

    first_name: {
      type: 'string',
      required: true
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

    city: {
      type: 'string',
      required: true
    },

    province: {
      type: 'string',
      required: true
    },

    postal_code: {
      type: 'string',
      required: true
    },

    phone_number: {
      type: 'string',
      required: false
    },

    fax_number: {
      type: 'string',
      required: false
    },

    project_title: {
      type: 'string',
      required: true
    },

    source_of_funding: {
      type: 'string',
      required: true
    },

    abstract: {
      type: 'string',
      required: true
    },

  },


  exits: {
    success:{
      responseType: 'view',
      viewTemplatePath: 'pages/message',
      description: 'return view for displaying tissue request form'
    }
  },


  fn: async function (inputs, exits) {

    let data = {
      title: inputs.title,
      first_name: inputs.first_name,
      last_name: inputs.last_name,
      email: inputs.email,
      institution: inputs.institution,
      department_name: inputs.department_name,
      city: inputs.city,
      province: inputs.province,
      postal_code: inputs.postal_code,
      phone_number: inputs.phone_number,
      fax_number: inputs.fax_number,
      project_title: inputs.project_title,
      source_of_funding: inputs.source_of_funding,
      abstract: inputs.abstract,
      received_date: moment().format('YYYY-MM-DD')
    };
    let url = sails.config.custom.data_api_url + 'add_new_tissue_requests/';

    request.post({
      url: url,
      formData: data,
      'headers': {
        'Authorization': 'Token ' + this.req.session.auth_token
      }
      },
      function optionalCallback(err, httpResponse, body) {
        let message_title = "";
        let message_body = "";

        if (err) {
          message_title = "Error";
          message_body = 'Servers are down, please contact site admin for the help.';
          return exits.success({'msg_title': message_title, 'msg_body': message_body});
        }
        else if (httpResponse.statusCode === 400){
          message_title = "Error";
          message_body = "Invalid inputs, Please try again!";
          return exits.success({'msg_title': message_title, 'msg_body': message_body});
        }
        else {
          const response = JSON.parse(body);
          let tissue_request_number = moment().format('YYYYMMDD-') + String(response.tissue_requests_id).padStart(4, '0');
          message_title = "Confirmation";
          message_body = "Your data is received, kindly note down following tissue request number for reference: " +
            tissue_request_number + ". " +
            "Also, please email following documents: CV, ethics, tissue request template in order to process your request";
          return exits.success({'msg_title': message_title, 'msg_body': message_body});
        }
      });

  }


};
