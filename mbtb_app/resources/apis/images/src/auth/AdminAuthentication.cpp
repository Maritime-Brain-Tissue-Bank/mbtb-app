//
// Created by Nirav Jadeja on 2020-04-12.
//
#include <DBAdminAuthentication.h>
#include "AdminAuthentication.h"

AdminAuthentication::AdminAuthentication() = default;

AdminAuthentication::~AdminAuthentication() = default;

std::tuple<bool, std::string> AdminAuthentication::authenticate(http::http_headers messageHeaders) {
    if(messageHeaders.find("Authorization") == messageHeaders.end()){
        this->errorMsg_ = "Invalid token header. No credentials provided.";
        return std::make_tuple(false, this->errorMsg_);
    }

    auto authHeader_ = messageHeaders[header_names::authorization];
    std::string tokenName_ = authHeader_.substr(0, 5);

    if (tokenName_ != "Token"){
        this->errorMsg_ = "Invalid input. Only `Token` tag is allowed.";
        return std::make_tuple(false, this->errorMsg_);
    }
    auto tokenValue_ = authHeader_.substr(6, authHeader_.size());

    try{
        auto decodeObj_ = jwt::decode(tokenValue_, algorithms({this->adminAuthAlgorithm_}), secret(this->adminAuthSecret_));
        auto payload_ = decodeObj_.payload().create_json_obj();
        DBAdminAuthentication dbAdminAuthentication;
        auto db_response = dbAdminAuthentication.adminTokenAuth(payload_["id"], payload_["email"]);
        return db_response;

    } catch (const std::exception& e){
        this->errorMsg_ = "Admin Token Auth: " + std::string(e.what());
        std::cerr << this->errorMsg_ << std::endl;
        return std::make_tuple(false, this->errorMsg_);

    } catch(const jwt::DecodeError& e){
        this->errorMsg_ = "Admin Token Auth: can't decode the token.";
        std::cerr << this->errorMsg_ << " - " << e.what() << std::endl;
        return std::make_tuple(false, this->errorMsg_);

    }catch (const jwt::VerificationError& e) {
        this->errorMsg_ = "Admin Token Auth: can't verify the token.";
        std::cerr << this->errorMsg_ << " - " << e.what() << std::endl;
        return std::make_tuple(false, this->errorMsg_);

    } catch (...) {
        this->errorMsg_ = "Admin Token Auth: Caught unknown exception.";
        std::cerr << this->errorMsg_ << std::endl;  // logging
        return std::make_tuple(false, this->errorMsg_);
    }
}
