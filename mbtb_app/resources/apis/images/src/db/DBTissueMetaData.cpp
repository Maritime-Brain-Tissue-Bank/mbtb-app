//
// Created by Nirav Jadeja on 2020-04-08.
//

#include <DBTissueMetaData.h>

DBTissueMetaData::DBTissueMetaData()= default;

DBTissueMetaData::~DBTissueMetaData()= default;


std::vector<DBTissueMetaData::singleTissueMetaData> DBTissueMetaData::getData(int prime_details_id) {
    singleTissueMetaData tissueMetaData;
    DBConnection dbConnection("localhost", 33060, "mbtb_prod", "test", "test@123");
    auto sql_session = dbConnection.getConnection();
    sql_session.sql("SET @p_prime_details_id = ?;").bind(prime_details_id).execute();
    auto sql_result = sql_session.sql("CALL selectTissueMetaData(@p_prime_details_id)").execute();
    DBConnection::closeConnection(&sql_session);
    for (Row row: sql_result.fetchAll()){
        tissueMetaData.filename_ = row[0].get<std::string>();
        tissueMetaData.nRegionName = row[1].get<std::string>();
        tissueMetaData.stainName = row[2].get<std::string>();
        tissueMetaDataList.push_back(tissueMetaData);
    }
    return tissueMetaDataList;

}
