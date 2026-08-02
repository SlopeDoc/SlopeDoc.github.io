#include <colormap.glsl>

layout(location = 1) out vec4 oId;   // fragColor (location 0) is already declared

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution;
    fragColor = vec4(viridis(uv.x + 0.2 * sin(uv.y * 6.0 + iTime)), 1.0);

    // a stand-in for a real per-object id : an 8x8 checker of the same rect
    float cell = mod(floor(uv.x * 8.0) + floor(uv.y * 8.0), 2.0);
    oId = vec4(vec3(cell), 1.0);
}
