uniform sampler2D previous;

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution;
    vec3 prev = texture(previous, uv).rgb * 0.95;   // fade
    float add = 0.0;
    for (int i = 0; i < 3; ++i) {
        float t = iTime * (1.0 + 0.4 * float(i)) + float(i) * 2.094;   // 2pi/3 apart
        vec2 dot = 0.5 + 0.3 * vec2(cos(t), sin(t * 1.3));
        add += smoothstep(0.03, 0.0, length(uv - dot));
    }
    fragColor = vec4(prev + add, 1.0);
}
