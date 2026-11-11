#include <cstdint>
#include "Utilities/xBRZ/xbrz.h"
extern "C" void scale4(const uint32_t*src,uint32_t*dst,int w,int h){xbrz::scale(4,src,dst,w,h,xbrz::ColorFormat::ARGB);}
