//
// Created by Nirav Jadeja on 2020-04-06.
//

#include <iostream>
#include <DBConnection.h>

using namespace std;
using namespace DBConnect;

int main(int argc, const char * argv[]){

    DBConnection dbConnection("localhost", 33060, "mbtb_prod", "test", "test@123");
    auto schema = dbConnection.getConnection();

    Table table = schema.getTable("users");

    RowResult rowResult = table.select("id", "email", "first_name", "last_name").
            where("email like: email").
            bind("email", "temp@mbtb.ca").execute();

    Row row = rowResult.fetchOne();

    cout << " id: " << row[0] << "\n" << " email: " << row[1] << " \n"
         << " first_name: " << row[2] << "\n" << " last_name: " << row[3] << endl;

    dbConnection.closeConnection();

}