//
// Created by Nirav Jadeja on 2020-04-12.
//

#pragma once

#include <Controller.h>


class AdminAuthentication {

private:
    std::string adminAuthSecret_ = "SECRET_KEY";
    std::string adminAuthAlgorithm_ = "HS256";

public:
    AdminAuthentication();
    ~AdminAuthentication();

    static bool authenticate(http::http_headers messageHeaders);

};

