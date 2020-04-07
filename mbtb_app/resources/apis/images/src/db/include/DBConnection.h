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
        const char* hostName_;
        const char* schemaName_;
        const char* username_;
        const char* password_;
        int port_;
        Session * session_;

    public:
        DBConnection(const char* hostName, int port, const char* schemaName, const char* username, const char* password);
        ~DBConnection();

        Schema getConnection();
        void closeConnection();

    };
}

