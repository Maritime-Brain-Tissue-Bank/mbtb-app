//
// Created by Nirav Jadeja on 2020-04-03.
//

#include "basic_controller.h"

namespace rest {

    BasicController::BasicController() = default;

    void BasicController::setEndpoint(const std::string & value) {
        uri endpointURI(value);
        uri_builder endpointBuilder;

        endpointBuilder.set_scheme(endpointURI.scheme());
        endpointBuilder.set_host(endpointURI.host());
        endpointBuilder.set_port(endpointURI.port());
        endpointBuilder.set_path(endpointURI.path());

        _listener = http_listener(endpointBuilder.to_uri());
    }

    std::string BasicController::endpoint() const {
        return _listener.uri().to_string();
    }

    pplx::task<void> BasicController::accept() {
        initRestOpHandlers();
        return _listener.open();
    }

    pplx::task<void> BasicController::shutdown() {
        return _listener.close();
    }

}
