//
// Created by Nirav Jadeja on 2020-04-03.
//
#include <iostream>
#include <UserInterruptHandler.h>
#include <Router.h>

using namespace web;
using namespace rest;
using namespace std;

int main(int argc, const char * argv[]) {
    InterruptHandler::hookSIGINT();

    Router router;
    router.setEndpoint("http://127.0.0.1:7000/");  // setting server endpoint or base url here

    try {
        router.accept().wait();
        cout << "CZI Image server started at: " << router.endpoint() << '\n';

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
