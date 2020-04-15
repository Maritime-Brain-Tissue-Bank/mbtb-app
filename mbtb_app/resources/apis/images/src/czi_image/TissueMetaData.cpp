//
// Created by Nirav Jadeja on 2020-04-07.
//

#include <DBTissueMetaData.h>
#include <TissueMetaData.h>

TissueMetaData::TissueMetaData() = default;

TissueMetaData::~TissueMetaData() = default;

void TissueMetaData::getTissueMetaData(http::http_request * message, const std::string& prime_details_id) {
    // ToDo: Add pplx::task here  for concurrency, save resources to server other requests.
    DBTissueMetaData dbTissueMetaData;
    auto data = dbTissueMetaData.getData(std::stoi(prime_details_id));
    auto response = json::value::object();

    // validation: if data vector empty return 404.
    if (data.empty()){
        response["Error"] = json::value::string("Data not found.");
        message->reply(status_codes::NotFound, response);
    }

    int id_count = 0;
    for (auto & i : data){
        response["meta_data"][id_count]["prime_details_id"] = i.primeDetailsID_;
        response["meta_data"][id_count]["file_name"] = json::value::string(i.filename_);
        response["meta_data"][id_count]["n_region_name"] = json::value::string(i.nRegionName);
        response["meta_data"][id_count]["stain_name"] = json::value::string(i.stainName);
        id_count++;
    }
    message->reply(status_codes::OK, response);
}