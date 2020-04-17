//
// Created by Nirav Jadeja on 2020-04-13.
//

#pragma once

#include <DBConnection.h>

using namespace DBConnect;

class DBAdminAuthentication{
private:
    struct adminAuth{
        int adminAuthID_;
        std::string adminAuthEmail_;
    } adminAuth;

public:
    DBAdminAuthentication();
    ~DBAdminAuthentication();

    bool isAdmin(int adminID_, const std::string& adminEmail_);
};
