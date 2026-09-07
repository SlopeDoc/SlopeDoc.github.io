// Hand-edited: a dashed stroke whose colour sweeps across the board.
// Delete this file and slope writes the plain default back.
#include <plot.glsl>
uniform sampler2D samples;
uniform vec2  span;
uniform vec4  color;
uniform float line_width, reveal;

void main() {
    vec2 px = iPixelXY(), p = iWorld();
    float d = sdGraph(p, dataAt(samples, span, p.x),
                         dataSlope(samples, span, p.x), px);

    float u = (p.x - span.x) / (span.y - span.x);            // 0..1 across the frame
    vec3  rgb = mix(vec3(0.16, 0.53, 0.94), vec3(0.95, 0.42, 0.22), u);

    float a = color.a
            * stroke(d, line_width * 1.5)
            * dashMask(p, vec2(15.0, 9.0), px)                // dash, gap, in pixels
            * inSpan(p.x, span, px.x)
            * revealMask(p.x, span, reveal, px.x);
    fragColor = vec4(rgb, a);
}
