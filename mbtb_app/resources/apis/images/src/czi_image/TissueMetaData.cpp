//
// Created by Nirav Jadeja on 2020-04-07.
//

#include <DBTissueMetaData.h>
#include <TissueMetaData.h>

TissueMetaData::TissueMetaData() = default;

TissueMetaData::~TissueMetaData() = default;

void TissueMetaData::getTissueMetaData(http::http_request * message, const std::string& prime_details_id) {
    // ToDo: Add pplx::task here  for concurrency, save resources to server other requests.
    DBTissueMetaData::getData(std::stoi(prime_details_id));

    std::string temp = "mbtb_code value: " + prime_details_id;
    auto response = json::value::object();
    response["Controller"] = json::value::string("TempController");
    response["message"] = json::value::string(temp);
    message->reply(status_codes::OK, response);
}