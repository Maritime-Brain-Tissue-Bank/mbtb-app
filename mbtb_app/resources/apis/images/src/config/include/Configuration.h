//
// Created by Nirav Jadeja on 2020-05-08.
//

#pragma once

#include <iostream>
#include <filesystem>

class Configuration{

public:
    static const std::string environment;
    static const std::string hostName;
    static const std::string port;
    static const std::string dbFile;
    static const std::string appDir;
    static const std::string currentBuildDir;

    static const float zoomLevel;


};
