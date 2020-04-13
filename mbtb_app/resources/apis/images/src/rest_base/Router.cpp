//
// Created by Nirav Jadeja on 2020-04-07.
//

#include <Router.h>

using namespace web;
using namespace http;

namespace rest{

    void Router::initRestOpHandlers() {
        listener_.support(methods::GET, std::bind(&Router::handleGet, this, std::placeholders::_1));
        listener_.support(methods::PUT, std::bind(&Router::handlePut, this, std::placeholders::_1));
        listener_.support(methods::POST, std::bind(&Router::handlePost, this, std::placeholders::_1));
        listener_.support(methods::DEL, std::bind(&Router::handleDelete, this, std::placeholders::_1));
        listener_.support(methods::PATCH, std::bind(&Router::handlePatch, this, std::placeholders::_1));
    }

    void Router::handleGet(http_request message) {
        auto path = requestPath(message);
        if (!path.empty() && path[0] == "czi_image"){ //  route: {base}/czi_image
            CZIController::run(&message);
        }
        if (!path.empty() && path[0] == "tissue_meta_data" && !path[1].empty()){  // route: {base}/tissue_meta_data
            std::string primeDetailsID_ = path[1];
            pplx::create_task([&message, primeDetailsID_](){
                TissueMetaData::getTissueMetaData(&message, primeDetailsID_);
            }).wait();

        }
        else{  //  route: {base}/
            auto response = json::value::object();
            response["message"] = json::value::string("Welcome to the image api");
            message.reply(status_codes::OK, response);
        }
    }

    void Router::handlePost(http_request message) {
        auto response = json::value::object();
        response["status"] = json::value::string("okay");
        response["message"] = json::value::string("POST test");
        message.reply(status_codes::OK, response);
    }


    void Router::handlePut(http_request message) {
        message.reply(status_codes::NotImplemented, responseNotImpl(methods::PUT));
    }


    void Router::handlePatch(http_request message) {
        message.reply(status_codes::NotImplemented, responseNotImpl(methods::PATCH));
    }


    void Router::handleDelete(http_request message) {
        message.reply(status_codes::NotImplemented, responseNotImpl(methods::DEL));
    }

    void Router::handleHead(http_request message) {
        message.reply(status_codes::NotImplemented, responseNotImpl(methods::HEAD));
    }

    void Router::handleOptions(http_request message) {
        message.reply(status_codes::NotImplemented, responseNotImpl(methods::OPTIONS));
    }

    void Router::handleTrace(http_request message) {
        message.reply(status_codes::NotImplemented, responseNotImpl(methods::TRCE));
    }

    void Router::handleConnect(http_request message) {
        message.reply(status_codes::NotImplemented, responseNotImpl(methods::CONNECT));
    }

    void Router::handleMerge(http_request message) {
        message.reply(status_codes::NotImplemented, responseNotImpl(methods::MERGE));
    }

    json::value Router::responseNotImpl(const http::method & method) {
        auto response = json::value::object();
        response["api_name"] = json::value::string("CZI Image");
        response["message"] = json::value::string("Method not implemented.");
        response["http_method"] = json::value::string(method);
        return response ;
    }
}