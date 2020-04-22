//
// Created by Nirav Jadeja on 2020-04-03.
//

#include "CZIController.h"

CZIController::CZIController() = default;

CZIController::~CZIController() = default;

void CZIController::run(http::http_request * message) {
    auto response = json::value::object();
    response["Controller"] = json::value::string("CZIController");
    response["message"] = json::value::string("Inside CZI - check");
    message->reply(status_codes::OK, response);
}

void CZIController::processImage() {
    std::string fileURL_ = this->baseDir_ + "samples/" + this->fileName_;
    std::wstring wFileURL_ = std::wstring(fileURL_.begin(), fileURL_.end());

    auto stream = libCZI::CreateStreamFromFile(wFileURL_.c_str());
    auto cziReader = libCZI::CreateCZIReader();
    cziReader->Open(stream);
    auto statistics = cziReader->GetStatistics();

    // get the display-setting from the document's metadata
    auto mds = cziReader->ReadMetadataSegment();
    auto md = mds->CreateMetaFromMetadataSegment();
    auto docInfo = md->GetDocumentInfo();
    auto dsplSettings = docInfo->GetDisplaySettings();

    auto x = statistics.boundingBox.x;
    auto y = statistics.boundingBox.y ;
    auto width = statistics.boundingBox.w;
    auto height = statistics.boundingBox.h;
    libCZI::IntRect roi{x, y, width, height}; // setting region of interest

    // get the tile-composite for all channels (which are marked 'active' in the display-settings)
    std::vector<std::shared_ptr<libCZI::IBitmapData>> actvChBms;
    int index = 0;  // index counting only the active channels
    std::map<int, int> activeChNoToChIdx;   // we need to keep track which 'active channels" corresponds to which channel index
    auto accessor = cziReader->CreateSingleChannelScalingTileAccessor();
    libCZI::CDisplaySettingsHelper::EnumEnabledChannels(dsplSettings.get(),
                                [&](int chIdx)->bool
                                {
                                    libCZI::CDimCoordinate planeCoord{ { libCZI::DimensionIndex::C, chIdx } };
                                    actvChBms.emplace_back(accessor->Get(roi, &planeCoord, 0.05f, nullptr));
                                    activeChNoToChIdx[chIdx] = index++;
                                    return true;
                                });

    // initialize the helper with the display-settings and provide the pixeltypes
    // (for each active channel)
    libCZI::CDisplaySettingsHelper dsplHlp;
    dsplHlp.Initialize(dsplSettings.get(),
                       [&](int chIdx)->libCZI::PixelType { return actvChBms[activeChNoToChIdx[chIdx]]->GetPixelType(); });

    // pass the tile-composites we just created (and the display-settings for the those active
    //  channels) into the multi-channel-composor-function
    auto mcComposite = libCZI::Compositors::ComposeMultiChannel_Bgr24(
            dsplHlp.GetActiveChannelsCount(),
            std::begin(actvChBms),
            dsplHlp.GetChannelInfosArray());

    // setting file and converting it to wstring
    std::string outputFileURL_ = this->baseDir_ + "cache/" + this->imageDir_ + this->tissueDetails_[2] + ".png";
    std::wstring wOutputFile_ = std::wstring(outputFileURL_.begin(), outputFileURL_.end());

    CSaveData cSaveData(wOutputFile_, SaveDataFormat::PNG);
    cSaveData.Save(mcComposite.get());
}

void CZIController::getImage(const std::string& filename) {
    this->fileName_ = filename;
    getTissueDetails();

    // ToDo : need a private method here to check or create directories for unix system
    auto status_ = createOrCheckDirs();
    if (status_){
        std::cout << "status: true" << status_;
        processImage();
    }
    else{
        std::cout << "status: false" << status_;
    }

}

// this method is to find image from cache
void CZIController::findImage() {

}

// This methods splits recieved filename string and store mbtb_code, region and stain name in the vector tissueDetails_
void CZIController::getTissueDetails(){
    std::stringstream ss(this->fileName_);
    std::string item;
    char delim = ' ';  // delimeter to split string i.e. single white space here.
    while(std::getline(ss, item, delim)) {
        this->tissueDetails_.push_back(item.substr(1, item.size()));
    }

    // removing .czi file extension from last element of vector tissueDetails_.
    this->tissueDetails_[2] = this->tissueDetails_[2].substr(0, this->tissueDetails_[2].find(".czi"));
    this->imageDir_ = this->tissueDetails_[0] + "/" + this->tissueDetails_[1] + "/";
}


// this method is to check if directories exist or not. If not then create it for png images for related region names and stains
// return boolean value accordingly.
bool CZIController::createOrCheckDirs() {
    std::string dir_ = this->baseDir_ + "cache/" +this->imageDir_;
    if (mkdir(dir_.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH) == 0)
    {
        // return true if dirs are created.
        return true;
    }
    else{
        // if dirs exist return true or throw runtime exception
        if( errno == EEXIST ) {
            return true;
        } else {
            std::cout << "Error: cannot create directories for " << this->imageDir_ << strerror(errno) << std::endl;
            throw std::runtime_error( strerror(errno) );
        }
    }
}
