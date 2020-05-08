//
// Created by Nirav Jadeja on 2020-04-03.
//
#include <iostream>
#include <Configuration.h>
#include <UserInterruptHandler.h>
#include <Router.h>

using namespace web;
using namespace rest;
using namespace std;

int main(int argc, const char * argv[]) {
    InterruptHandler::hookSIGINT();

    Router router;
    std::string uri = "http://" + Configuration::hostName + ":" + Configuration::port + "/";  // server base url
    router.setEndpoint(uri);

    try {
        router.accept().wait();
        cout << "*********" << endl;
        cout << "CZI Image server started at: " << router.endpoint() << endl;

        InterruptHandler::waitForUserInterrupt();

        router.shutdown().wait();
    }
    catch(exception & e) {

        cerr << "Error: " << e.what() << endl;

    }
    catch(...) {

        cerr << "Unknown failure occurred, Possible memory corruption" << endl;
    }

    return 0;
}
