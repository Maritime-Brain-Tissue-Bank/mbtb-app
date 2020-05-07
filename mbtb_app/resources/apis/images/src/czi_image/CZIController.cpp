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

// This method is to process czi image and convert it to png format
void CZIController::processImage() {
    std::string fileURL_ = this->baseDir_ + "samples/" + this->fileName_ + ".czi";
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

                                    //  NOTE: zoom level controls image resolution here; its value is from 0 to 1; now it is set to 20%.
                                    actvChBms.emplace_back(accessor->Get(roi, &planeCoord, 0.20f, nullptr));
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

std::string CZIController::getImage(const std::string& filename) {
    this->fileName_ = filename;
    getTissueDetails();

    auto imageStatus_ = isImageExist();
    std::string pngImage_ = this->baseDir_ + "cache/" +this->imageDir_ + this->tissueDetails_[2] +".png";

    // ToDo: write return views here based on response status (i.e. imageStatus_, status_)
    if (imageStatus_){
        std::cout << "Image is already there, return it from here" <<std::endl;
        return pngImage_;
    } else{

        auto dirStatus_ = createOrCheckDirs();
        if (dirStatus_){
            processImage();
            return pngImage_;
        }
        else{
            return "none";
            // ToDo: throw exception here
        }
    }

}

// This method checks if image already exists in the cache directory or not and return bool value.
bool CZIController::isImageExist() {
    std::string dir_ = this->baseDir_ + "cache/" + this->imageDir_ + "/" + this->tissueDetails_[2] + ".png";
    return std::__fs::filesystem::exists(dir_);
}

// This methods splits recieved filename string and store mbtb_code, region and stain name in the vector tissueDetails_
void CZIController::getTissueDetails(){
    std::stringstream ss(this->fileName_);
    std::string item;
    char delim = ' ';  // delimeter to split string i.e. single white space here.
    while(std::getline(ss, item, delim)) {
        this->tissueDetails_.push_back(item.substr(1, item.size()));
    }


    this->imageDir_ = this->tissueDetails_[0] + "/" + this->tissueDetails_[1] + "/";
}


// This method is to check if directories exist or not. If not then create it for png images for related region names and stains
// return boolean value accordingly.
bool CZIController::createOrCheckDirs() {
    std::string dir_ = this->baseDir_ + "cache/";
    bool dirStatus_ = false;  // bool flag for operation in for loop

    // creating dirs sequentially as mkdir don't create it at once with tissue name and region name
    for (int i = 0; i < 2; i++) {
        dir_.append(this->tissueDetails_[i]);
        if (mkdir(dir_.c_str(), S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH) == 0)
        {
            dir_.append("/");  // appending '/' at the end for sub dir
            dirStatus_ = true;
        }
        else{
            if( errno == EEXIST ) {
                dir_.append("/");  // appending '/' at the end for sub dir
                dirStatus_ = true;
            } else {
                std::cout << "Error: cannot create directories for " << this->imageDir_ << strerror(errno) << std::endl;
                throw std::runtime_error( strerror(errno) );
            }
        }
    }
    return dirStatus_;
}
