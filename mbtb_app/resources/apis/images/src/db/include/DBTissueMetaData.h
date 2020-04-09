//
// Created by Nirav Jadeja on 2020-04-08.
//

#pragma once

#include <DBConnection.h>
#include <TissueMetaData.h>

using namespace DBConnect;

class DBTissueMetaData{

private:

public:
    DBTissueMetaData();
    ~DBTissueMetaData();

    static void getData(int prime_details_id);
};
