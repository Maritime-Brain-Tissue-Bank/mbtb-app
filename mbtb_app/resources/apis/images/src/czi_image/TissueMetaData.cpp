//
// Created by Nirav Jadeja on 2020-04-07.
//

#include <DBTissueMetaData.h>
#include <TissueMetaData.h>

TissueMetaData::TissueMetaData(){
    this->idCount_ = 0;
};

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


    for (auto & i : data){

        this->currentNode_ = i.nRegionName;
        if (this->currentNode_ != this->previousNode_){
            this->idCount_ = 0;
            response[this->currentNode_][this->idCount_]["file_name"] = json::value::string(i.filename_);
            response[this->currentNode_][this->idCount_]["stain_name"] = json::value::string(i.stainName);
            this->previousNode_ = this->currentNode_;
            this->idCount_++;
        }
        else{
            response[this->currentNode_][this->idCount_]["file_name"] = json::value::string(i.filename_);
            response[this->currentNode_][this->idCount_]["stain_name"] = json::value::string(i.stainName);
            //cout << this->currentNode_ << " : " << i.stainName << " //\n";
            this->idCount_++;
        }
    }
    message->reply(status_codes::OK, response);
}