//
// Created by Nirav Jadeja on 2020-04-07.
//

#pragma once

#include <tuple>
#include <Controller.h>
#include <RestController.h>
#include <CZIController.h>
#include <TissueMetaData.h>
#include <Authentication.h>
#include <cpprest/filestream.h>


namespace rest{

    /*
     *  Router class implements rest methods and handle endpoint routing in api.
     */

    class Router : public Controller, RestController {

    public:

        Router() : Controller() {}

        void handleGet(http_request message) override;
        void handlePut(http_request message) override;
        void handlePost(http_request message) override;
        void handlePatch(http_request message) override;
        void handleDelete(http_request message) override;
        void handleHead(http_request message) override;
        void handleOptions(http_request message) override;
        void handleTrace(http_request message) override;
        void handleConnect(http_request message) override;
        void handleMerge(http_request message) override;
        void initRestOpHandlers() override;

    private:

        static json::value responseNotImpl(const http::method & method);
    };

}
