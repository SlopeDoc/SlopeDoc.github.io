// one texel = one particle : rg = position, ba = velocity
uniform sampler2D state;    // this shader's previous frame
uniform sampler2D field;    // the CPU field

layout(std430, binding = 0) buffer Density { uint density[]; };
layout(std430, binding = 1) buffer Peak    { uint peak[]; };

uniform float uAttract;

const float DT   = 0.008;
const float FIX  = 4096.0;
const int   GRID = 128;

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }

void main() {
    ivec2 id = ivec2(gl_FragCoord.xy);
    vec4 s = texelFetch(state, id, 0);
    vec2 p = s.xy, v = s.zw;

    if (iFrame < 1) {                     // seeded here, nothing uploaded at startup
        float a = 6.2831853 * hash(vec2(id));
        float r = 0.25 + 0.55 * hash(vec2(id) + 7.0);
        p = r * vec2(cos(a), sin(a));
        v = 0.9 * sqrt(r) * vec2(-sin(a), cos(a));
    }

    float w = texture(field, p * 0.5 + 0.5).r;
    vec2  g = -uAttract * p / pow(dot(p, p) + 0.01, 1.5);
    v += g * (1.0 + 3.0 * w) * DT;
    p += v * DT;

    ivec2 cell = ivec2((p * 0.5 + 0.5) * float(GRID));
    if (all(greaterThanEqual(cell, ivec2(0))) && all(lessThan(cell, ivec2(GRID)))) {
        uint before = atomicAdd(density[cell.y * GRID + cell.x], uint(FIX));
        atomicMax(peak[0], before + uint(FIX));       // the reduction
    }

    fragColor = vec4(p, v);               // the next frame's state
}
