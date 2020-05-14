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

            // ToDo: need exception handling here for file not found, etc

            // Fetching filename from json body from request and then pass to CZIController to get image name.
            auto image_ = pplx::create_task([=](){
                return message.extract_json();
            }).then([=](const pplx::task<json::value>& requestTask){
                auto request = requestTask.get();
                auto fileName_ = request.at("filename").as_string();
                if(request.at("has_meta_data").as_bool() == true){
                    json::object metaData_ = request.at("meta_data").as_object();
                    CZIController cziController;
                    auto image_ = cziController.getImage(fileName_, metaData_);
                    return image_;
                }
                else{
                    CZIController cziController;
                    auto image_ = cziController.getImage(fileName_);
                    return image_;
                }

            });

            // opening filestream and sending image to request
            concurrency::streams::fstream::open_istream(image_.get(), std::ios::in)
                    .then([=](const concurrency::streams::istream& is) {
                        // send the file when ready
                        message.reply(status_codes::OK, is, "image/png")
                                .then([image_](const pplx::task<void>& t) {
                                    // handle error in sending
                                    try { t.get();
                                    }
                                    catch(...) {
                                        std::cout << "error in sending" << "\n";
                                    } });
                    })
                    .then([=](const pplx::task<void>&t) {
                        // handle error in loading
                        try { t.get();
                        }
                        catch(...) {
                            std::cout << "error in Loading ---" << "\n";
                            message.reply(status_codes::InternalError);
                        }})
                    .wait();

        }
        if (!path.empty() && path[0] == "tissue_meta_data" && !path[1].empty()){  // route: {base}/tissue_meta_data
            std::string primeDetailsID_ = path[1];
            pplx::create_task([message]() -> std::tuple<bool, std::string>{

                // authenticating request
                const auto& messageHeaders_ = message.headers();
                Authentication authentication;
                auto response_ = authentication.authenticate(messageHeaders_);
                return response_;

            }).then([&message, primeDetailsID_](const pplx::task<std::tuple<bool, std::string>>& taskResult_){

                auto result_ = taskResult_.get();
                if (std::get<0>(result_) == false){
                    auto response_ = json::value::object();
                    response_["Error"] = json::value::string(std::get<1>(result_));
                    message.reply(status_codes::Unauthorized, response_);
                }
                else{
                    TissueMetaData tissueMetaData;
                    tissueMetaData.getTissueMetaData(&message, primeDetailsID_);
                }

            }).wait();

        }
        else{  //  route: {base}/
            auto response = json::value::object();
            response["message"] = json::value::string("Welcome to the image api");
            message.reply(status_codes::OK, response);
        }
    }

    void Router::handlePost(http_request message) {
        message.reply(status_codes::NotImplemented, responseNotImpl(methods::POST));
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