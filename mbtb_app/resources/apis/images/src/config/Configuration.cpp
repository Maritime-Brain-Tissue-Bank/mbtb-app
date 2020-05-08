//
// Created by Nirav Jadeja on 2020-05-08.
//
#include <Configuration.h>

const std::string Configuration::environment = "development";

const std::string Configuration::hostName = "127.0.0.1";

const std::string Configuration::port = "7000";

const std::string Configuration::appDir = "/Users/niravjadeja/Downloads/mbtb-app/mbtb_app/resources/apis/images/";

// ToDo: set the file name with extension accordingly.
const std::string Configuration::dbFile = appDir + "src/files/" + environment + "/db.cnf";

// Zoom level for image resolution; values between 0 to 1; now set to 20%.
const float Configuration::zoomLevel = 0.2f;
