
#ifndef __RGB_DEINTERLEAVE_H__
#define __RGB_DEINTERLEAVE_H__

extern int rgb_deinterleave_c(char* src, char* dst[3]);
extern int rgb_deinterleave_neon(char* src, char* dst[3]);

#endif /*__RGB_DEINTERLEAVE_H__ */
