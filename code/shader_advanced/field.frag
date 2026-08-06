uniform sampler2D source;

void main() {
    vec2 uv = gl_FragCoord.xy / iResolution;
    fragColor = vec4(texture(source, uv).rrr, 1.0);
}
