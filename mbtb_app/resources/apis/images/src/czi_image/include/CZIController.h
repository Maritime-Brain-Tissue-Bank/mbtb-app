//
// Created by Nirav Jadeja on 2020-04-03.
//

#pragma once

#include <Controller.h>

class CZIController{

public:
    CZIController();
    ~CZIController();

    static void run(http::http_request * message);

};
