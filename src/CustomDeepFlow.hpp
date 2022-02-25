#include "opencv2/core.hpp"
#include "opencv2/video.hpp"

#include "opencv2/optflow/pcaflow.hpp"
#include "opencv2/optflow/sparse_matching_gpc.hpp"

namespace cv
{
namespace optflow
{

class CV_EXPORTS_W CustomOpticalFlowDeepFlow: public cv::DenseOpticalFlow
{
public:
    CustomOpticalFlowDeepFlow();
    CustomOpticalFlowDeepFlow(float sigma, int minSize,
            float downscaleFactor, int fixedPointIterations, int sorIterations,
            float alpha, float delta, float gamma, float omega, int maxLayers,
            int interpolationType);

    void calc( cv::InputArray I0, cv::InputArray I1, cv::InputOutputArray flow );
    void collectGarbage();
    //Added SETters
    CV_WRAP virtual void setSigma(float val) { sigma = val; }
    CV_WRAP virtual void setMinSize(int val) { minSize = val; }
    CV_WRAP virtual void setDownscaleFactor(float val) { downscaleFactor = val; }
    CV_WRAP virtual void setFixedPointIterations(int val) { fixedPointIterations = val; }
    CV_WRAP virtual void setSorIterations(int val) { sorIterations = val; }
    CV_WRAP virtual void setAlpha(float val) { alpha = val; }
    CV_WRAP virtual void setDelta(float val) { delta = val; }
    CV_WRAP virtual void setGamma(float val) { gamma = val; }
    CV_WRAP virtual void setOmega(float val) { omega = val; }
    CV_WRAP virtual void setMaxLayers(int val) { maxLayers = val; }
    CV_WRAP virtual void setInterpolationType(int val) { interpolationType = val; }

protected:
    float sigma; // Gaussian smoothing parameter
    int minSize; // minimal dimension of an image in the pyramid
    float downscaleFactor; // scaling factor in the pyramid
    int fixedPointIterations; // during each level of the pyramid
    int sorIterations; // iterations of SOR
    float alpha; // smoothness assumption weight
    float delta; // color constancy weight
    float gamma; // gradient constancy weight
    float omega; // relaxation factor in SOR

    int maxLayers; // max amount of layers in the pyramid
    int interpolationType;


private:
    std::vector<cv::Mat> buildPyramid( const cv::Mat& src );

};
CV_EXPORTS_W cv::Ptr<DenseOpticalFlow> createOptFlow_CustomDeepFlow();
CV_EXPORTS_W cv::Ptr<CustomOpticalFlowDeepFlow> createCustomDeepFlow();

} // optflow
} // cv