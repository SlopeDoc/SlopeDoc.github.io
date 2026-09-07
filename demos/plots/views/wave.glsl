#include <plot.glsl>
uniform sampler2D samples;
uniform vec2  span;
uniform vec4  color;
uniform float line_width, reveal;

void main() {
    vec2 px = iPixelXY(), p = iWorld();
    float a = color.a
            * stroke(sdGraph(p, dataAt(samples, span, p.x),
                                dataSlope(samples, span, p.x), px), line_width)
            * inSpan(p.x, span, px.x)
            * revealMask(p.x, span, reveal, px.x);
    fragColor = vec4(color.rgb, a);
}
