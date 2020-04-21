//
// Created by Nirav Jadeja on 2020-04-20.
//
#include <iostream>
#include <IncLIBCZI.h>
#include <CZIController.h>

using namespace std;
using namespace libCZI;

int main(){

    CZIController cziController;
    cziController.getImage("#bb00-003 #n10 #cod.czi");
}