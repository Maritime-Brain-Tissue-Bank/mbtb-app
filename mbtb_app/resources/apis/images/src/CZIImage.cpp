//
// Created by Nirav Jadeja on 2020-04-03.
//
#include <iostream>
#include <user_interrupt_handler.h>
#include "czi_controller.h"
#include <mysqlx/xdevapi.h>

using namespace mysqlx;

using namespace web;
using namespace rest;
using namespace std;

int main(int argc, const char * argv[]) {
    InterruptHandler::hookSIGINT();

    CZIController server;
    server.setEndpoint("http://127.0.0.1:7000/czi_image");

    try {
        server.accept().wait();
        cout << "CZI Image server started at: " << server.endpoint() << '\n';

        InterruptHandler::waitForUserInterrupt();

        server.shutdown().wait();
    }
    catch(exception & e) {

        cerr << "Error: " << e.what() << endl;

    }
    catch(...) {

        cerr << "Unknown failure occurred, Possible memory corruption" << endl;
    }

    return 0;
}
