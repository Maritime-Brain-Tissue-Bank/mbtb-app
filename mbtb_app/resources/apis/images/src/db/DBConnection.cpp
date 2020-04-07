//
// Created by Nirav Jadeja on 2020-04-06.
//

#include <DBConnection.h>


namespace DBConnect{

    DBConnection::DBConnection(const char* hostName, int port, const char* schemaName, const char* username, const char* password):
                hostName_(hostName), port_(port), schemaName_(schemaName), username_(username), password_(password)
    {

    }

    Schema DBConnection::getConnection() {
        cout << "Creating new DB connection to schema: " << this->schemaName_ << endl;
        session_ = new Session(this->hostName_, this->port_, this->username_, this->password_);
        Schema schema_ = session_->getSchema(this->schemaName_);
        return schema_;
    }

    void DBConnection::closeConnection(){
        cout << "Closing DB Connection" << endl;
        this->session_->close();  // Closing session with DB
        delete session_;  // Deleting session instance, freeing memory
    }

    DBConnection::~DBConnection() {
    }

}