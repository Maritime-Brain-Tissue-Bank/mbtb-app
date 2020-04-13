//
// Created by Nirav Jadeja on 2020-04-08.
//

#pragma once

#include <DBConnection.h>
#include <TissueMetaData.h>

using namespace DBConnect;

class DBTissueMetaData{

private:
    // for converting fetched row
    struct singleTissueMetaData{
        int primeDetailsID_;
        std::string filename_;
        std::string nRegionName;
        std::string stainName;
    };
    std::vector<singleTissueMetaData> tissueMetaDataList;

public:
    DBTissueMetaData();
    ~DBTissueMetaData();

    std::vector<DBTissueMetaData::singleTissueMetaData> getData(int prime_details_id);
};
