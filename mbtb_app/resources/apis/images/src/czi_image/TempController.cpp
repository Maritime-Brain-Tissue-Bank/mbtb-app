//
// Created by Nirav Jadeja on 2020-04-07.
//

#include "TempController.h"

TempController::TempController() = default;

TempController::~TempController() = default;

void TempController::run(http_request * message) {
    auto response = json::value::object();
    response["Controller"] = json::value::string("TempController");
    response["message"] = json::value::string("Inside Temp ********");
    message->reply(status_codes::OK, response);
}