//
// Created by Nirav Jadeja on 2020-04-06.
//

#pragma once

#include <iostream>
#include <mysqlx/xdevapi.h>

using namespace std;
using namespace mysqlx;

namespace DBConnect{

    class DBConnection{

    private:
        int _port;
        std::string _dburl;
        std::string _username;
        std::string _password;

    public:
        DBConnection(std::string url, int port, std::string username, std::string password);

        void get_data(const std::string & schema_name);


    };
}

