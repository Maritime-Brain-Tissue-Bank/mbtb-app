//
// Created by Nirav Jadeja on 2020-04-06.
//

#include <iostream>
#include <DBConnection.h>

using namespace std;
using namespace DBConnect;

int main(int argc, const char * argv[]){

    DBConnection dbConnection("localhost", 33060, "test", "test@123");

    dbConnection.get_data("mbtb_prod");

}