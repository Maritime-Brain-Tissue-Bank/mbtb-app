const request = require('request');

module.exports = {


  friendlyName: 'Insert single row data',


  description: '',


  inputs: {
    mbtb_code: {
      type: 'string',
      required: true
    },

    sex: {
      type: 'string',
      required: true
    },

    age: {
      type: 'string',
      required: true
    },

    race: {
      type: 'string',
      required: false
    },

    cause_of_death: {
      type: 'string',
      required: true
    },

    postmortem_interval: {
      type: 'string',
      required: true
    },

    brain_weight: {
      type: 'number',
      required: true
    },

    time_in_fix: {
      type: 'string',
      required: true
    },

    neuoropathology_diagnosis: {
      type: 'string',
      required: true
    },

    neuoropathology_detailed: {
      type: 'string',
      required: false
    },

    neuoropathology_gross: {
      type: 'string',
      required: false
    },

    neuoropathology_micro: {
      type: 'string',
      required: false
    },

    neuoropathology_criteria: {
      type: 'string',
      required: false
    },

    cerad: {
      type: 'string',
      required: false
    },

    braak_stage: {
      type: 'string',
      required: false
    },

    khachaturian: {
      type: 'string',
      required: false
    },

    abc: {
      type: 'string',
      required: false
    },

    clinical_diagnosis: {
      type: 'string',
      required: true
    },

    duration: {
      type: 'number',
      required: true
    },

    clinical_history: {
      type: 'string',
      required: false
    },

    autopsy_type: {
      type: 'string',
      required: true
    },

    tissue_type: {
      type: 'string',
      required: true
    },

    storage_method: {
      type: 'string',
      required: true
    },

    formalin_fixed: {
      type: 'string',
      required: true
    },

    fresh_frozen: {
      type: 'string',
      required: true
    },

  },


  exits: {
    bad_combo: {
      responseType: 'view',
      viewTemplatePath: 'pages/add_new_data',
      description: 'return view for password mismatch, display error msg'
    }
  },


  fn: async function (inputs, exits) {

    let payload = {
      mbtb_code: inputs.mbtb_code,
      sex: inputs.sex,
      age: inputs.age,
      postmortem_interval: inputs.postmortem_interval,
      time_in_fix: inputs.time_in_fix,
      tissue_type: inputs.tissue_type,
      storage_method: inputs.storage_method,
      autopsy_type: inputs.autopsy_type,
      neuoropathology_diagnosis: inputs.neuoropathology_diagnosis,
      race: inputs.race,
      diagnosis: inputs.clinical_diagnosis,
      duration: inputs.duration,
      clinical_history: inputs.clinical_history,
      cause_of_death: inputs.cause_of_death,
      brain_weight: inputs.brain_weight,
      neuoropathology_detailed: inputs.neuoropathology_detailed,
      neuropathology_gross: inputs.neuoropathology_gross,
      neuropathology_micro: inputs.neuoropathology_micro,
      neouropathology_criteria: inputs.neuoropathology_criteria,
      cerad: inputs.cerad,
      braak_stage: inputs.braak_stage,
      khachaturian: inputs.khachaturian,
      abc: inputs.abc,
      formalin_fixed: inputs.formalin_fixed,
      fresh_frozen: inputs.fresh_frozen
    };

    let url = sails.config.custom.data_api_url + 'add_new_data/';

    // post request to insert single row in db via api with admin auth token
    request.post({
        url: url,
        formData: payload,
        'headers': {
          'Authorization': 'Token ' + this.req.session.admin_auth_token_val,
          }
          },
      function optionalCallback(err, httpResponse, body) {
        if (err) {
          console.log({'error_msg': err}); // log error to server console
        }
        else {

          try {
            const response = JSON.parse(body);
            if(typeof (response) == "object"){
              return exits.bad_combo({'error_msg': response.Error}) // display error msg for wrong email, password
            }
          }
          catch (e) {
            return exits.success();
          }

        }
      });

  }


};
