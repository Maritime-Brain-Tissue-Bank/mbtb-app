//
// Created by Nirav Jadeja on 2020-04-17.
//

#pragma once

#include <DBConnection.h>

using namespace DBConnect;

class DBUserAuthentication{

private:
    struct userAuth{
        int userID_;
        std::string userAuthEmail_;
    } userAuth;

public:
    DBUserAuthentication();
    ~DBUserAuthentication();

    bool isUser(int userID_, const std::string& userEmail_);
};
