var app = angular
    .module("DetailsApp", [])
    .controller("DetailsController", function ($scope) {
        var detail = [{
            id: "1",
            race: "CAUCASIAN",
            diagnosis_of_dementia: "AD",
            duration_of_dementia: "9",
            clinical_history: "DEMENTIA 9 YEARS",
            cause_of_death: "",
            brain_weight: "1175",
            neuropathology_detailed: "1. DEFINITE ALZHEIMER DISEASE WITH (A) CEREBRAL ATROPHY (1175G) (B) NEURONAL LOSS AND GLIOSIS (C) PLAQUES 30 PER MPF IN TEMPORAL LOBE (D) NEUROFIBRILLARY TANGLES SCATTERED (E) CEREBELLAR CORTICAL DEGENERATION MILD.  2. VASCULAR PATHOLOGY WITH (A) INFARCTS, MULTIPLE, SUBACUTE, IN FRONTAL, TEMPORAL AND PARIETAL LOBES AND PUTAMEN (B) ATHEROSCLEROSIS MODERATE BASAL CEREBRAL VESSELS (C) PALLOR OF FRONTAL WHITE MATTER (D) VASCULAR PROLIFERATION (E) MILD HYALINIZATION.",
            neuropathology_gross: "",
            neuropathology_micro: "",
            neuropathology_criteria: "KHACHATURIAN",
            cerad: "",
            braak_stage: "",
            KHACHATURIAN: "30",
            abc: "",
            autopsy_type: "brain",
            tissue_Type: "brain"

        },];

        $scope.details = detail;

    });

