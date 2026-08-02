#include <sdf.glsl>
#include <colormap.glsl>

// (x, y, vx, vy) per particle, updated on the CPU side every frame and
// re-uploaded — see main.cpp's updater
layout(std430, binding = 0) buffer Particles { vec4 p[]; };

void main() {
    vec2 uv = (gl_FragCoord.xy / iResolution) * 2.0 - 1.0;
    uv.x *= iAspect;

    vec3 col = vec3(1.0);
    for (int i = 0; i < 8; ++i) {
        float d = sdCircle(uv - p[i].xy, 0.09);
        vec3 c = hsv2rgb(vec3(fract(float(i) * 0.618034), 0.75, 0.9));
        col = mix(c, col, smoothstep(0.0, 0.015, d));
    }
    fragColor = vec4(col, 1.0);
}
