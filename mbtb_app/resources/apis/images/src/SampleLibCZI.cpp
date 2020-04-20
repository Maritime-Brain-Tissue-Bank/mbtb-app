//
// Created by Nirav Jadeja on 2020-04-20.
//
#include <iostream>
#include <INCLIBCZI.h>

using namespace std;
using namespace libCZI;

int main(){
    auto stream = libCZI::CreateStreamFromFile(LR"(/Users/niravjadeja/Downloads/mbtb-app/mbtb_app/resources/apis/images/src/images/samples/3.czi)");
    auto spReader = libCZI::CreateCZIReader();
    spReader->Open(stream);

    spReader->EnumerateSubBlocks(
            [&](int idx, const SubBlockInfo& info)->bool
            {
                if (idx > 500 && idx < 510){
                    auto sbBlk = spReader->ReadSubBlock(idx);
                    auto bitmap = sbBlk->CreateBitmap();
                    cout << "Index " << idx << ": " << libCZI::Utils::DimCoordinateToString(&info.coordinate) << " Rect=" << info.logicalRect << endl;

                    //WrtImage(idx, bitmap.get());

                    return true;
                }
                return true;
            });
}