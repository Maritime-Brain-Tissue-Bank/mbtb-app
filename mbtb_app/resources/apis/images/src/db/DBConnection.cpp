//
// Created by Nirav Jadeja on 2020-04-06.
//

#include <DBConnection.h>


namespace DBConnect{

    DBConnection::DBConnection(const char* hostName, int port, const char* schemaName, const char* username, const char* password):
                hostName_(hostName), port_(port), schemaName_(schemaName), username_(username), password_(password)
    {
    }

    Session DBConnection::getConnection() {
        std::cout << "Creating new DB connection to schema: " << this->schemaName_ << endl;
        Session session_(this->hostName_, this->port_, this->username_, this->password_);
        session_.sql("USE mbtb_prod;").execute();  // ToDo: set schema name dynamically here.
        return session_;
    }

    void DBConnection::closeConnection(Session * session_){
        std::cout << "Closing DB Connection" << endl;
        session_->close();  // Closing session with DB
    }

    DBConnection::~DBConnection() = default;

}