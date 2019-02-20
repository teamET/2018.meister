#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highguui.hpp>
#include <iostream>

int main(int argc,const char* argv[]){
    cv::Mat src=cv::imread("sample.jpg",cv::IMREAD_COLOR);

    if(src.empty()){
        std::cerr<<"Failed to open image file."<<std::endl;
        return -1;
    }else{
        std::cerr<<"success to open image file."<<std::endl;
    }


    return 0;
}

