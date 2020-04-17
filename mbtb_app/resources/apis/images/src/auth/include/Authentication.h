//
// Created by Nirav Jadeja on 2020-04-17.
//

#pragma once

#include <Controller.h>
#include <jwt/jwt.hpp>

using namespace jwt::params;

class Authentication{

private:
    std::string authSecretkey_ = "SECRET_KEY";
    std::string jwtAlgorithm_ = "HS256";
    std::string errorMsg_ = "None";

public:
    Authentication();
    ~Authentication();

    std::tuple<bool, std::string> authenticate(http::http_headers messageHeaders);
};
