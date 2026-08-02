#include <camera.glsl>
#include <sdf.glsl>
#include <raymarch.glsl>

// spot.obj sits roughly in [-0.5,0.5]x[-0.7,1.0]x[-0.7,1.0] : this floats an
// animated blob just beside it, so orbiting shows real occlusion
float sceneSDF(vec3 p) {
    vec3 q = p - vec3(0.9, 0.3, 0.0);
    float a = sdSphere(q, 0.22);
    vec3 orbit = vec3(0.22 * sin(iTime), 0.22 * cos(iTime), 0.0);
    float b = sdSphere(q - orbit, 0.13);
    return opSmoothUnion(a, b, 0.15);
}

void main() {
    vec3 ro, rd; polyscopeRay(ro, rd);
    vec3 pos;
    if (marchScene(ro, rd, pos) && visibleOverScene(pos)) {
        vec3 n = sceneNormal(pos);
        fragColor = vec4(shadeDefault(pos, n, rd, vec3(0.85, 0.25, 0.25), vec3(1.0)), 1.0);
    } else {
        discard;   // let the mesh show through instead
    }
}
