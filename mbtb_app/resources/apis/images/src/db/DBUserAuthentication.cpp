//
// Created by Nirav Jadeja on 2020-04-17.
//

#include <DBUserAuthentication.h>

DBUserAuthentication::DBUserAuthentication() = default;

DBUserAuthentication::~DBUserAuthentication() = default;

bool DBUserAuthentication::isUser(int userID_, const std::string &userEmail_) {
    std::cout << "***** User Authentication *****" <<std::endl;

    DBConnection dbConnection("localhost", 33060, "mbtb_prod", "test", "test@123");
    auto sql_session = dbConnection.getConnection();
    sql_session.sql("SET @p_user_auth_id = ?, @p_user_auth_email = ?;").bind(userID_, userEmail_).execute();
    auto sql_result = sql_session.sql("CALL selectUserAuthToken(@p_user_auth_id, @p_user_auth_email)").execute();
    DBConnection::closeConnection(&sql_session);
    auto result_count_ = sql_result.count();

    for (Row row: sql_result.fetchAll()){
        userAuth.userID_ = row[0];
        userAuth.userAuthEmail_ = row[1].get<std::string>();
    }

    // ToDo: Need a proper validation here based on cpp standards.
    if (result_count_ == 1 && userAuth.userAuthEmail_ != ""){
        return true;
    }

    return false;
}
