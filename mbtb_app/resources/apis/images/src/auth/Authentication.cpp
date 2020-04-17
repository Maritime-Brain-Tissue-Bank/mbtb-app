//
// Created by Nirav Jadeja on 2020-04-17.
//

#include <DBAdminAuthentication.h>
#include <DBUserAuthentication.h>
#include <Authentication.h>

Authentication::Authentication() = default;

Authentication::~Authentication() = default;

std::tuple<bool, std::string> Authentication::authenticate(http::http_headers messageHeaders) {
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
        DBAdminAuthentication adminAuthentication;
        DBUserAuthentication userAuthentication;

        auto decodeObj_ = jwt::decode(tokenValue_, algorithms({this->jwtAlgorithm_}), secret(this->authSecretkey_));
        auto payload_ = decodeObj_.payload().create_json_obj();

        // if admin - return true
        if (adminAuthentication.isAdmin(payload_["id"], payload_["email"])){
            return std::make_tuple(true, this->errorMsg_);
        }

        // if user - return true
        if (userAuthentication.isUser(payload_["id"], payload_["email"])){
            return std::make_tuple(true, this->errorMsg_);
        }

        this->errorMsg_ = "Error: authentication failed, user not found.";
        return std::make_tuple(false, this->errorMsg_);

    } catch (const std::exception& e){
        this->errorMsg_ = "Error: " + std::string(e.what());
        std::cerr << this->errorMsg_ << std::endl;
        return std::make_tuple(false, this->errorMsg_);

    } catch(const jwt::DecodeError& e){
        this->errorMsg_ = "Error: can't decode the auth token.";
        std::cerr << this->errorMsg_ << " - " << e.what() << std::endl;
        return std::make_tuple(false, this->errorMsg_);

    }catch (const jwt::VerificationError& e) {
        this->errorMsg_ = "Error: can't verify the auth token.";
        std::cerr << this->errorMsg_ << " - " << e.what() << std::endl;
        return std::make_tuple(false, this->errorMsg_);

    } catch (...) {
        this->errorMsg_ = "Error: Caught unknown exception during token authentication";
        std::cerr << this->errorMsg_ << std::endl;  // logging
        return std::make_tuple(false, this->errorMsg_);
    }
}
