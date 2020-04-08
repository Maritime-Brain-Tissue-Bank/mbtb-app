//
// Created by Nirav Jadeja on 2020-04-07.
//

#pragma once

#include <Controller.h>

using namespace web;

class TempController{

public:
    TempController();
    ~TempController();

    static void run(http_request * message);

};


