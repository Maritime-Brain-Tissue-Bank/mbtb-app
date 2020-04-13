//
// Created by Nirav Jadeja on 2020-04-12.
//
#include <DBAdminAuthentication.h>
#include "AdminAuthentication.h"

AdminAuthentication::AdminAuthentication() = default;

AdminAuthentication::~AdminAuthentication() = default;

bool AdminAuthentication::authenticate(http::http_headers messageHeaders) {
    if(messageHeaders.find("Authorization") == messageHeaders.end()){
        return false;
    }

    auto authHeader_ = messageHeaders[header_names::authorization];
    std::string tokenName_ = authHeader_.substr(0, 5);

    if (tokenName_ != "Token"){
        return false;
    }
    auto tokenValue_ = authHeader_.substr(6, authHeader_.size());

    try{
        auto decodeObj_ = jwt::decode(tokenValue_, algorithms({this->adminAuthAlgorithm_}), secret(this->adminAuthSecret_));
        auto payload_ = decodeObj_.payload().create_json_obj();
        DBAdminAuthentication dbAdminAuthentication;
        auto db_response = dbAdminAuthentication.adminTokenAuth(payload_["id"], payload_["email"]);
        return db_response;

    } catch(const jwt::DecodeError& e){
        std::cerr << "Admin Token Auth: Decode Error - " << e.what() << std::endl;

    }catch (const jwt::VerificationError& e) {
        std::cerr << "Admin Token Auth: Verification Error - " << e.what() << std::endl;

    } catch (...) {
        std::cerr << "Admin Token Auth: Caught unknown exception\n";
    }



    // ToDo: authenticate tokenValue_ here with jwt and compare it with DB, return bool value
    return false;
}
