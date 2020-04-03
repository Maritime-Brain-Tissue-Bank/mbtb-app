//
// Created by Nirav Jadeja on 2020-04-03.
//

#pragma once

#include "string"
#include "cpprest/http_listener.h"
#include "pplx/pplxtasks.h"
#include "rest_controller.h"

using namespace web;
using namespace http::experimental::listener;

namespace rest{

    class BasicController{

    protected:
        http_listener _listener; // main network endpoint for service

    public:
        BasicController();

        void setEndpoint(const std::string &value);
        std::string endpoint() const;

        pplx::task<void> accept();
        pplx::task<void> shutdown();

        virtual void initRestOpHandlers(){
            /* have to be implemented by the child class */
        }

    };
}