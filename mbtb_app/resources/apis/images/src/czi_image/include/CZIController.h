//
// Created by Nirav Jadeja on 2020-04-03.
//

#pragma once

#include <Controller.h>
#include <IncLIBCZI.h>
#include <IncCZICMD.h>

using namespace libCZI;

class CZIController{

private:
    std::string baseDir_ = "/Users/niravjadeja/Downloads/mbtb-app/mbtb_app/resources/apis/images/src/images/";
    std::string outputPath_ = "";


    void processImage(const std::string& filename_);
    void findImage();

public:
    CZIController();
    ~CZIController();

    static void run(http::http_request * message);
    void getImage(const std::string& filename_);

};
