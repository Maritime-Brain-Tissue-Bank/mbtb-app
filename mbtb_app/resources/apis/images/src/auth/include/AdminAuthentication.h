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

public:
    AdminAuthentication();
    ~AdminAuthentication();

    bool authenticate(http::http_headers messageHeaders);

};

