//
// Created by Nirav Jadeja on 2020-04-08.
//

#include <DBTissueMetaData.h>

DBTissueMetaData::DBTissueMetaData()= default;;

DBTissueMetaData::~DBTissueMetaData()= default;;


void DBTissueMetaData::getData(int prime_details_id) {
    DBConnection dbConnection("localhost", 33060, "mbtb_prod", "test", "test@123");
    auto sql_session = dbConnection.getConnection();
    sql_session.sql("SET @p_prime_details_id = ?;").bind(prime_details_id).execute();
    auto sql_result = sql_session.sql("CALL selectTissueMetaData(@p_prime_details_id)").execute();
    for (Row row: sql_result.fetchAll()){
        cout << row[0] << " " << row[1] << " " << row[2] << endl;
    }
    dbConnection.closeConnection(&sql_session);

}
