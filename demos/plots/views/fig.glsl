#include <plot.glsl>
uniform vec4  background, grid_color, axis_color;
uniform vec2  grid_step;
uniform vec2  axis_at;       // where x = 0 and y = 0 fall, far off a log axis
uniform float line_width;
uniform vec3  show;          // grid, axes, frame, 1 when drawn

void main() {
    vec2 px = iPixelXY(), p = iWorld();
    vec2 lo = iViewCenter - iViewHalf, hi = iViewCenter + iViewHalf;
    Ink k = inkClear();
    inkOver(k, axis_color.rgb, axis_color.a *
            max(show.y * axesMask(p - axis_at, px, 1.5*line_width),
                show.z * frameMask(p, lo, hi, px, line_width)));
    inkOver(k, grid_color.rgb, grid_color.a * show.x * gridMask(p, grid_step, px, 0.7*line_width));
    inkOver(k, background.rgb, background.a);
    fragColor = inkResolve(k);
}
