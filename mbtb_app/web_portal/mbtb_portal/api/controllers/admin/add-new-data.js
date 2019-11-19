module.exports = {


  friendlyName: 'Add new data',


  description: `It redirects to the "admin_add_new_data" template and load data for dropdowns i.e. autopsy_type, tissue_type
                , storage_methods, sex, disease_names`,


  inputs: {

  },


  exits: {
    success: {
      viewTemplatePath: 'pages/admin_add_new_data',
      locals: {
        layout: 'layouts/admin_layout'
      }
    }
  },


  fn: async function (inputs, exits) {

    var sex = ['Male', 'Female'];
    var neuro_diagnosis = ['TAUOPATHY', 'MIXED AD LBD', 'MIXED AD DS'];
    var autopsy_type = ['Brain', 'Full Body', 'Brain & Spinal'];
    var tissue_type = ['Brain', 'Spinal Cord', 'Ocular'];
    var storage_methods = ['Formalin-Fixed', 'Fresh Frozen', 'Both'];
    var boolean_values = ['True', 'False'];
    return exits.success({sex: sex, neuro_diagnosis: neuro_diagnosis, autopsy_type:autopsy_type, tissue_type:tissue_type,
      storage_method: storage_methods, boolean_values: boolean_values});

  }


};
