//
// Created by Nirav Jadeja on 2020-04-07.
//

#pragma once

#include <Controller.h>



class TissueMetaData{

private:
    std::string currentNode_;
    std::string previousNode_;
    int idCount_;

public:
    TissueMetaData();
    ~TissueMetaData();

    void getTissueMetaData(http::http_request * message, const std::string& prime_details_id);

};


