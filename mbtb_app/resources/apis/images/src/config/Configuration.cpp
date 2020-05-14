//
// Created by Nirav Jadeja on 2020-05-08.
//
#include <Configuration.h>

const std::string Configuration::environment = "development";

const std::string Configuration::hostName = "127.0.0.1";

const std::string Configuration::port = "7000";

// this will give following path: {root dir}/images/build
const std::string Configuration::currentBuildDir = std::__fs::filesystem::current_path();

// appDir is root dir of repo i.e. {root dir}/images/
const std::string Configuration::appDir = currentBuildDir.substr(0, currentBuildDir.length()-5);

// ToDo: set the file name with extension accordingly.
const std::string Configuration::dbFile = appDir + "src/files/" + environment + "/db.cnf";

// Zoom level for image resolution; values between 0 to 1; now set to 20%.
const float Configuration::zoomLevel = 0.05f;
