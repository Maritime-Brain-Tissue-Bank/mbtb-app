//
// Created by Nirav Jadeja on 2020-04-03.
//

#pragma once

#include <Configuration.h>
#include <Controller.h>
#include <IncLIBCZI.h>
#include <IncCZICMD.h>

using namespace libCZI;

class CZIController{

private:
    std::string baseDir_ = Configuration::appDir + "src/images/";
    std::string fileName_;
    std::string imageDir_;
    std::vector<std::string> tissueDetails_;

    void processImage();
    bool isImageExist();
    void getTissueDetails();
    bool createOrCheckDirs();

public:
    CZIController();
    ~CZIController();

    static void run(http::http_request * message);
    std::string getImage(const std::string& filename_);

};
