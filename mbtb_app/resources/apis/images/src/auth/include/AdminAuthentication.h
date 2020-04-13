//
// Created by Nirav Jadeja on 2020-04-12.
//

#pragma once

#include <Controller.h>
#include <jwt/jwt.hpp>

using namespace jwt::params;

class AdminAuthentication {

private:
    std::string adminAuthSecret_ = "SECRET_KEY";
    std::string adminAuthAlgorithm_ = "HS256";
    std::string errorMsg_ = "None";

public:
    AdminAuthentication();
    ~AdminAuthentication();

    std::tuple<bool, std::string> authenticate(http::http_headers messageHeaders);

};

