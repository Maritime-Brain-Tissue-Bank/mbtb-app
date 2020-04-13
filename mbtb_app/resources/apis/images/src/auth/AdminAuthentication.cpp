//
// Created by Nirav Jadeja on 2020-04-12.
//

#include "AdminAuthentication.h"

AdminAuthentication::AdminAuthentication() = default;

AdminAuthentication::~AdminAuthentication() = default;

bool AdminAuthentication::authenticate(http::http_headers messageHeaders) {
    if(messageHeaders.find("Authorization") == messageHeaders.end()){
        return false;
    }

    auto authHeader_ = messageHeaders[header_names::authorization];
    std::string tokenName_ = authHeader_.substr(0, 5);

    if (tokenName_ == "Token"){
        return false;
    }
    auto tokenValue_ = authHeader_.substr(6, authHeader_.size());

    // ToDo: authenticate tokenValue_ here with jwt and compare it with DB, return bool value
    return false;
}
