#include <colormap.glsl>

layout(std430, binding = 0) buffer Density { uint density[]; };

uniform float uPeak;

const float FIX  = 4096.0;
const int   GRID = 128;

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution;
    ivec2 cell = clamp(ivec2(uv * float(GRID)), ivec2(0), ivec2(GRID - 1));
    float d = float(density[cell.y * GRID + cell.x]) / FIX;
    fragColor = vec4(inferno(clamp(d / uPeak, 0.0, 1.0)), 1.0);
}
