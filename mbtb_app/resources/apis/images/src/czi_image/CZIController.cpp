//
// Created by Nirav Jadeja on 2020-04-03.
//

#include "CZIController.h"

using namespace web;
using namespace http;

void CZIController::initRestOpHandlers() {
    listener_.support(methods::GET, std::bind(&CZIController::handleGet, this, std::placeholders::_1));
    listener_.support(methods::PUT, std::bind(&CZIController::handlePut, this, std::placeholders::_1));
    listener_.support(methods::POST, std::bind(&CZIController::handlePost, this, std::placeholders::_1));
    listener_.support(methods::DEL, std::bind(&CZIController::handleDelete, this, std::placeholders::_1));
    listener_.support(methods::PATCH, std::bind(&CZIController::handlePatch, this, std::placeholders::_1));
}

void CZIController::handleGet(http_request message) {
    auto response = json::value::object();
    response["status"] = json::value::string("okay");
    response["message"] = json::value::string("GET test");
    message.reply(status_codes::OK, response);
}

void CZIController::handlePost(http_request message) {
    auto response = json::value::object();
    response["status"] = json::value::string("okay");
    response["message"] = json::value::string("POST test");
    message.reply(status_codes::OK, response);
}


void CZIController::handlePut(http_request message) {
    message.reply(status_codes::NotImplemented, responseNotImpl(methods::PUT));
}


void CZIController::handlePatch(http_request message) {
    message.reply(status_codes::NotImplemented, responseNotImpl(methods::PATCH));
}


void CZIController::handleDelete(http_request message) {
    message.reply(status_codes::NotImplemented, responseNotImpl(methods::DEL));
}

void CZIController::handleHead(http_request message) {
    message.reply(status_codes::NotImplemented, responseNotImpl(methods::HEAD));
}

void CZIController::handleOptions(http_request message) {
    message.reply(status_codes::NotImplemented, responseNotImpl(methods::OPTIONS));
}

void CZIController::handleTrace(http_request message) {
    message.reply(status_codes::NotImplemented, responseNotImpl(methods::TRCE));
}

void CZIController::handleConnect(http_request message) {
    message.reply(status_codes::NotImplemented, responseNotImpl(methods::CONNECT));
}

void CZIController::handleMerge(http_request message) {
    message.reply(status_codes::NotImplemented, responseNotImpl(methods::MERGE));
}

json::value CZIController::responseNotImpl(const http::method & method) {
    auto response = json::value::object();
    response["api_name"] = json::value::string("CZI Image");
    response["message"] = json::value::string("Method not implemented.");
    response["http_method"] = json::value::string(method);
    return response ;
}