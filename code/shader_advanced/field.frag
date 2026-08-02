void main() {
    vec2 uv = gl_FragCoord.xy / iResolution;
    fragColor = vec4(texture(iChannel0, uv).rrr, 1.0);
}
