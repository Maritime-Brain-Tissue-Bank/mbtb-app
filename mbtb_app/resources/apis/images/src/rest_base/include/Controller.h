//
// Created by Nirav Jadeja on 2020-04-03.
//

#pragma once

#include "string"
#include "cpprest/http_listener.h"
#include "pplx/pplxtasks.h"
#include "RestController.h"

using namespace web;
using namespace http::experimental::listener;

namespace rest{

    class Controller{

    protected:
        http_listener listener_; // main network endpoint for service

    public:
        Controller();

        void setEndpoint(const std::string &value);
        std::string endpoint() const;

        pplx::task<void> accept();
        pplx::task<void> shutdown();

        virtual void initRestOpHandlers(){}

        static std::vector<utility::string_t> requestPath(const http_request & message);

    };
}