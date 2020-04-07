//
// Created by Nirav Jadeja on 2020-04-03.
//

#include "Controller.h"

namespace rest {

    Controller::Controller() = default;

    void Controller::setEndpoint(const std::string & value) {
        uri endpointURI(value);
        uri_builder endpointBuilder;

        endpointBuilder.set_scheme(endpointURI.scheme());
        endpointBuilder.set_host(endpointURI.host());
        endpointBuilder.set_port(endpointURI.port());
        endpointBuilder.set_path(endpointURI.path());

        listener_ = http_listener(endpointBuilder.to_uri());
    }

    std::string Controller::endpoint() const {
        return listener_.uri().to_string();
    }

    pplx::task<void> Controller::accept() {
        initRestOpHandlers();
        return listener_.open();
    }

    pplx::task<void> Controller::shutdown() {
        return listener_.close();
    }

}
