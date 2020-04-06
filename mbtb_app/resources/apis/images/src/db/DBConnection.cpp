//
// Created by Nirav Jadeja on 2020-04-06.
//

#include <DBConnection.h>


namespace DBConnect{

    DBConnection::DBConnection(std::string url, int port, std::string username, std::string password):
                    _dburl(std::move(url)), _port(port), _username(std::move(username)), _password(std::move(password))
                {
                }


    void DBConnection::get_data(const std::string & schema_name) {
        cout << "Creating SQL Connection...\n";

        Session session(_dburl, _port, _username, _password);

        Schema schema = session.getSchema(schema_name);

        Table table = schema.getTable("users");

        RowResult rowResult = table.select("id", "email", "first_name", "last_name").
                where("email like: email").
                bind("email", "temp@mbtb.ca").execute();

        Row row = rowResult.fetchOne();

        cout << " id: " << row[0] << "\n" << " email: " << row[1] << " \n"
             << " first_name: " << row[2] << "\n" << " last_name: " << row[3] << endl;
    }

}