#include <colormap.glsl>

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution;
    float v = texture(iChannel0, uv).r;
    fragColor = vec4(viridis(v), 1.0);
}
