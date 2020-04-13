//
// Created by Nirav Jadeja on 2020-04-13.
//
#include <DBAdminAuthentication.h>

DBAdminAuthentication::DBAdminAuthentication() = default;

DBAdminAuthentication::~DBAdminAuthentication() = default;

std::tuple<bool, std::string> DBAdminAuthentication::adminTokenAuth(int adminID_, const std::string& adminEmail_) {
    DBConnection dbConnection("localhost", 33060, "mbtb_prod", "test", "test@123");
    auto sql_session = dbConnection.getConnection();
    sql_session.sql("SET @p_admin_auth_id = ?, @p_admin_auth_email = ?;").bind(adminID_, adminEmail_).execute();
    auto sql_result = sql_session.sql("CALL selectAdminAuthToken(@p_admin_auth_id, @p_admin_auth_email)").execute();
    DBConnection::closeConnection(&sql_session);
    for (Row row: sql_result.fetchAll()){
        adminAuth.adminAuthID_ = row[0];
        adminAuth.adminAuthEmail_ = row[1].get<std::string>();
    }

    // ToDo: Need a proper validation here based on cpp standards.
    if (sizeof(adminAuth.adminAuthID_) == 0 || adminAuth.adminAuthEmail_ == ""){
        return std::make_tuple(false, "Admin Token Auth: Admin not found.");
    }
    return std::make_tuple(true, "None");

}
