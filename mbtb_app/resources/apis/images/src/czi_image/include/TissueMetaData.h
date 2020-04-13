//
// Created by Nirav Jadeja on 2020-04-07.
//

#pragma once

#include <Controller.h>



class TissueMetaData{

public:
    TissueMetaData();
    ~TissueMetaData();

    static void getTissueMetaData(http::http_request * message, const std::string& prime_details_id);

};


