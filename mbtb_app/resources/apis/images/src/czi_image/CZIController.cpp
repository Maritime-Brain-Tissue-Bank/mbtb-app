//
// Created by Nirav Jadeja on 2020-04-03.
//

#include "CZIController.h"

CZIController::CZIController() = default;

CZIController::~CZIController() = default;

void CZIController::run(http_request * message) {
    auto response = json::value::object();
    response["Controller"] = json::value::string("CZIController");
    response["message"] = json::value::string("Inside CZI - check");
    message->reply(status_codes::OK, response);
}
