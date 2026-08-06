#include <colormap.glsl>

uniform sampler2D field;

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution;
    float v = texture(field, uv).r;
    fragColor = vec4(viridis(v), 1.0);
}
