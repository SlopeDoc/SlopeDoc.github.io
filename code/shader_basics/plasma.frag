void main() {
    vec2 uv = gl_FragCoord.xy / iResolution;
    float v = sin(uv.x * 10.0 + iTime)
            + sin(uv.y * 10.0 + iTime * 1.3)
            + sin((uv.x + uv.y) * 10.0 + iTime * 0.7)
            + sin(length(uv - 0.5) * 20.0 - iTime * 2.0);
    fragColor = vec4(0.5 + 0.5 * sin(v * 1.5707 + vec3(0.0, 2.0, 4.0)), 1.0);
}
