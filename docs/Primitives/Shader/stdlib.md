---
title: A Shader "STL" 
---

Most shaders use a fairly common codebase (Inigo's sdfs, colormaps, camera handling, etc...). To avoid having to recode everything everytime, slope offers common shader functions!

Here are the current existing functions, and small examples, that you can include in Slope shaders:

=== "camera.glsl"

    | Function | |
    | --- | --- |
    | `lookAtRay(ro, target, lens, out rd)` | ray through this pixel for a camera at `ro` looking at `target` |
    | `orbitRayAt(orbit, radius, target, out ro, out rd)` | camera on a sphere around `target`, `orbit` = (yaw, pitch) in 0..1 |
    | `orbitRayTarget(radius, target, out ro, out rd)` | driven by the cursor while hovered, a fixed 3/4 view otherwise |
    | `orbitRay(out ro, out rd)` | `orbitRayTarget` with a stock radius/target |
    | `polyscopeNDC()` | this fragment's position in polyscope's normalised device coordinates |
    | `polyscopeRay(out ro, out rd)` | the ray polyscope itself would trace through this fragment |
    | `polyscopeDepth(world_pos)` | depth of a world point, in polyscope's depth-buffer convention |
    | `sceneDepthHere()` | polyscope's depth at this fragment (1.0 = nothing drawn there) |
    | `visibleOverScene(world_pos)` | is `world_pos` visible in front of polyscope's geometry |
    | `sceneEyeDistance()` | linear eye-space distance to polyscope's geometry here |
    | `sceneClearance(world_pos)` | signed distance (world units) from `world_pos` to the 3D scene |
    | `sceneOcclusion(world_pos, fade)` | soft occlusion, 0..1, easing over `fade` world units |
    | `sceneWorldPos()` | world-space position of the 3D scene's surface at this fragment |

    An orbit-camera raymarch, no C++ camera setup involved:

    ```glsl
    #include <sdf.glsl>
    #include <raymarch.glsl>

    float sceneSDF(vec3 p) {
        return opSmoothUnion(sdSphere(p, 1.0), sdPlane(p, vec3(0,1,0), 1.0), 0.3);
    }

    void main() {
        vec3 ro, rd;
        orbitRay(ro, rd);
        vec3 pos;
        vec3 col = vec3(1.0);
        if (marchScene(ro, rd, pos))
            col = shadeDefault(pos, sceneNormal(pos), rd, vec3(0.8), vec3(1.0));
        fragColor = vec4(col, 1.0);
    }
    ```

    The same scene, registered to polyscope's camera and occluded by real meshes instead (see [The 3D Scene](../scene); calling `visibleOverScene` here is what turns depth compositing on, no C++ needed):

    ```glsl
    #include <camera.glsl>
    #include <sdf.glsl>
    #include <raymarch.glsl>

    float sceneSDF(vec3 p) { return sdSphere(p - vec3(0,1,0), 0.6); }

    void main() {
        vec3 ro, rd; polyscopeRay(ro, rd);
        vec3 pos;
        if (marchScene(ro, rd, pos) && visibleOverScene(pos))
            fragColor = vec4(shadeDefault(pos, sceneNormal(pos), rd, vec3(0.8), vec3(1.0)), 1.0);
        else
            discard;   // let the 3D scene show through
    }
    ```

=== "sdf.glsl"

    Signed distance fields: negative inside, zero on the surface, positive outside.

    **2D**

    | Function | |
    | --- | --- |
    | `sdCircle(p, r)` | |
    | `sdBox2(p, half_size)` | |
    | `sdRoundBox2(p, half_size, r)` | uniform corner radius |
    | `sdSegment2(p, a, b)` | |
    | `sdNgon(p, r, n)` | regular n-gon, circumradius r |
    | `sdTriangle(p, p0, p1, p2)` | exact, any winding |
    | `sdArc(p, sc, ra, rb)` | ring wedge; `sc` = (sin,cos) of the half-aperture |
    | `sdPie(p, c, r)` | filled pie slice; `c` = (sin,cos) of the half-aperture |

    **3D**

    | Function | |
    | --- | --- |
    | `sdSphere(p, r)` | |
    | `sdPlane(p, n, h)` | |
    | `sdBox(p, half_size)` | |
    | `sdRoundBox(p, half_size, r)` | uniform corner radius |
    | `sdTorus(p, t)` | `t` = (major radius, minor radius) |
    | `sdCapsule(p, a, b, r)` | |
    | `sdCylinder(p, h, r)` | capped, y-axis |
    | `sdCappedCone(p, a, b, ra, rb)` | frustum between two points; either radius may be 0 for a plain cone |
    | `sdRoundCone(p, a, b, r1, r2)` | like `sdCapsule` but tapered, smooth tip |
    | `sdEllipsoid(p, r)` | bound, not exact; `r` = the three semi-axes |

    **Combining**

    | Function | |
    | --- | --- |
    | `opUnion(a, b)` / `opIntersect(a, b)` / `opSubtract(a, b)` | `b` minus `a` |
    | `opSmoothUnion(a, b, k)` / `opSmoothIntersect(a, b, k)` / `opSmoothSubtract(a, b, k)` | filleted by `k` |
    | `opShell(d, t)` | hollow shell, thickness `2t` |
    | `opRound(d, r)` | rounds any field's sharp edges, apply before combining |

    **Domain**

    | Function | |
    | --- | --- |
    | `opRepeat(p, c)` / `opRepeat2(p, c)` | tile space with period `c` |
    | `opMirrorX(p)` | mirror across x = 0 |
    | `opRotateY(p, a)` / `opRotate2(p, a)` | |

    A capped cone, a round cone and an ellipsoid, over a checkered ground (see the `raymarch.glsl` tab):

    ```glsl
    #include <sdf.glsl>
    #include <raymarch.glsl>

    float sceneSDF(vec3 p) {
        float cone   = sdCappedCone(p - vec3(-1.7, -0.7, 0.0), vec3(0), vec3(0, 1.2, 0), 0.6, 0.25);
        float rcone  = sdRoundCone (p - vec3( 0.0, -0.7, 0.0), vec3(0), vec3(0, 1.2, 0), 0.6, 0.1);
        float ell    = sdEllipsoid (p - vec3( 1.7,  0.05, 0.0), vec3(0.7, 0.45, 0.5));
        float ground = sdPlane(p, vec3(0,1,0), 0.7);
        return opUnion(opUnion(opUnion(cone, rcone), ell), ground);
    }

    void main() {
        vec3 ro, rd;
        orbitRayTarget(7.0, vec3(0.0), ro, rd);
        vec3 col = vec3(1.0);
        vec3 pos;
        if (marchScene(ro, rd, pos)) {
            vec3 n = sceneNormal(pos);
            float chk = checker(pos.xz, 0.5);
            col = shadeDefault(pos, n, rd, mix(vec3(0.85), vec3(0.55), chk), vec3(1.0));
        }
        fragColor = vec4(col, 1.0);
    }
    ```

    The 2D primitives, drawn flat, no raymarching, just a sign test:

    ```glsl
    #include <sdf.glsl>

    void main() {
        vec2 uv = (gl_FragCoord.xy / iResolution) * 2.0 - 1.0;
        uv.x *= iAspect;
        vec2 p = uv * 2.2;

        float tri = sdTriangle(p - vec2(-1.5, 0.0), vec2(-0.6,-0.5), vec2(0.6,-0.5), vec2(0.0,0.7));
        float arc = sdArc(p, vec2(sin(0.9), cos(0.9)), 0.7, 0.12);
        float pie = sdPie(p - vec2(1.5, 0.0), vec2(sin(1.0), cos(1.0)), 0.7);

        vec3 col = vec3(1.0);
        col = mix(col, vec3(0.85,0.2,0.2), 1.0 - smoothstep(0.0, 0.01, tri));
        col = mix(col, vec3(0.2,0.55,0.9), 1.0 - smoothstep(0.0, 0.01, arc));
        col = mix(col, vec3(0.2,0.75,0.35), 1.0 - smoothstep(0.0, 0.01, pie));
        fragColor = vec4(col, 1.0);
    }
    ```

=== "raymarch.glsl"

    Sphere tracing over an SDF, plus the shading terms that make the result read as a rendering rather than a depth map. Every shader including this one must define `sceneSDF(vec3 p)`: the functions here call it, so leaving it undefined is a link error even if you never call them yourself.

    | Function | |
    | --- | --- |
    | `marchScene(ro, rd, out pos)` | walks the ray to the surface; returns whether it hit |
    | `marchDistance(ro, rd)` | distance along the ray, or `MARCH_MAX_DIST` if it escaped |
    | `sceneNormal(p)` | the SDF's gradient, by central differences |
    | `softShadow(ro, rd, mint, maxt, sharpness)` | penumbra comes free from the distance field |
    | `ambientOcclusion(p, n)` | how enclosed a point is |
    | `fresnel(rd, n, power)` | grazing-angle rim light |
    | `checker(p, scale)` | checkerboard in world-space plane coordinates |
    | `shadeDefault(p, n, rd, albedo, light_dir)` | one key light, soft shadow, ambient, rim |

    `MARCH_STEPS` / `MARCH_MAX_DIST` / `MARCH_EPS` are `#define`s, overridable before the `#include` if the defaults march too coarse or too far for your scene. See the `sdf.glsl` tab above for a full scene using these.

=== "noise.glsl"

    Hash-based: no textures, no seeds, and the same input always gives the same output, which is exactly what makes it safe to use inside a ping-pong feedback loop.

    | Function | |
    | --- | --- |
    | `hash11(p)` / `hash12(p)` / `hash13(p)` | scalar hash, float/vec2/vec3 input |
    | `hash22(p)` / `hash33(p)` | vec2/vec3 hash |
    | `valueNoise(p)` | 2D or 3D, quintic-interpolated lattice hash |
    | `gradientNoise(p)` | Perlin-style, -1..1 |
    | `fbm(p, octaves)` | fractal sum of `valueNoise`, 2D or 3D |
    | `ridgedFbm(p, octaves)` | creases instead of blobs |
    | `domainWarp(p, octaves, strength)` | warp the domain by more noise |
    | `worley(p)` | (nearest, second-nearest) cell-point distance |
    | `curlNoise(p, eps)` | divergence-free 2D flow |

    ```glsl
    #include <noise.glsl>

    void main() {
        vec2 uv = gl_FragCoord.xy / iResolution;
        float n = fbm(uv * 6.0 + iTime * 0.1, 5);
        fragColor = vec4(vec3(n), 1.0);
    }
    ```

=== "colormap.glsl"

    Scientific colour maps, as polynomial fits over `t` in 0..1. The sequential ones are perceptually uniform (equal steps in `t` read as equal steps in brightness), which a raw hue ramp never gives you for free.

    | Function | |
    | --- | --- |
    | `viridis(t)` / `magma(t)` / `inferno(t)` / `plasma(t)` / `turbo(t)` | perceptually uniform sequential maps (except turbo) |
    | `grayscale(t)` | |
    | `coolwarm(t)` | diverging, neutral colour at `t = 0.5` |
    | `cosinePalette(t, offset, amp, freq, phase)` | Inigo Quilez's cosine-gradient formula, tunes a whole custom scheme from four vectors |
    | `remap(v, lo, hi)` | maps `v` to 0..1 across `[lo, hi]` |
    | `signedRemap(v, amplitude)` | signed `v` to 0..1, zero at 0.5, for a diverging map |
    | `hsv2rgb(c)` | for an angle: phase, orientation, winding. Hue isn't perceptually ordered, so a poor choice for a plain scalar |
    | `isoline(v, spacing, grad, width_px)` | 1 on the isolines of `v`, constant pixel width |

    ```glsl
    #include <colormap.glsl>

    void main() {
        float density = gl_FragCoord.x / iResolution.x;
        fragColor = vec4(viridis(density), 1.0);
    }
    ```

=== "complex.glsl"

    Complex arithmetic on `vec2` (x = real, y = imaginary), and domain colouring, the standard way to put an entire complex function on one picture. Includes `<colormap.glsl>` for `hsv2rgb`, so its names are in scope here too.

    | Function | |
    | --- | --- |
    | `cadd` / `csub` / `cmul` / `cdiv` / `cinv` / `cconj` | arithmetic |
    | `carg(a)` / `cabs(a)` | argument, modulus |
    | `cexp(a)` / `clog(a)` | |
    | `cpow(a, k)` / `cpow(a, b)` / `csqrt(a)` | real or complex exponent |
    | `csin(a)` / `ccos(a)` / `ctan(a)` | |
    | `mobius(z, a, b, c, d)` | (az+b)/(cz+d) |
    | `domainColor(w)` | hue = argument, brightness bands at doublings of `\|w\|` |
    | `domainColorGrid(w, spokes)` | `domainColor` plus argument contour lines |

    ```glsl
    #include <complex.glsl>
    #include <plot2d.glsl>

    void main() {
        vec2 z = plotPoint(-2.0, 2.0);
        vec2 w = cdiv(csub(cpow(z, 3.0), ONE), cadd(cmul(z, z), ONE));
        fragColor = vec4(domainColorGrid(w, 12), 1.0);
    }
    ```

=== "plot2d.glsl"

    Graphs and grids in plot coordinates, with line widths that stay put in pixels however the plot ends up scaled.

    | Function | |
    | --- | --- |
    | `unitsPerPixel(xmin, xmax)` | plot units covered by one pixel |
    | `plotPoint(xmin, xmax)` / `plotPointAt(xmin, xmax, ycenter)` | this fragment's position in plot coordinates |
    | `graphDist(y, fx, dfx)` | distance to the graph `y = f(x)`, first order |
    | `stroke(d, hw, aa)` | 1 inside a stroke of half-width `hw` |
    | `curveMask(p, fx, dfx, width_px, upp)` | a curve of constant pixel width |
    | `pointMask(p, center, r_px, upp)` | a filled disc marker, for scatter data |
    | `PLOT_SLOPE(f, x, upp)` | macro: slope of `f` at `x` by central differences |
    | `gridMask` / `gridMaskMinor(p, spacing, ...)` | grid lines, optionally coarse-over-fine |
    | `axesMask(p, upp)` | the two axes |
    | `xTickMask` / `yTickMask(p, spacing, len_px, upp)` | tick marks |
    | `underCurve(p, fx, upp)` | 1 below the graph |
    | `betweenCurves(p, lo, hi, upp)` | 1 between two graphs |

    ```glsl
    #include <plot2d.glsl>

    void main() {
        float upp = unitsPerPixel(-4.0, 4.0);
        vec2  p   = plotPoint(-4.0, 4.0);
        vec3 col = vec3(1.0);
        col = mix(col, vec3(0.85), 0.6 * gridMask(p, 1.0, upp));
        col = mix(col, vec3(0.0),  axesMask(p, upp));
        col = mix(col, vec3(0.8,0.1,0.1), curveMask(p, sin(p.x), cos(p.x), 3.0, upp));
        col = mix(col, vec3(0.1,0.3,0.8), pointMask(p, vec2(1.5, sin(1.5)), 5.0, upp));
        fragColor = vec4(col, 1.0);
    }
    ```

=== "slide.glsl"

    Sugar over the `TimeObject` uniforms and keyframe `#define`s from the [basics](../basics#following-the-talk) page, so a shader can stage itself against the talk with none of it spelled out by hand.

    | Function | |
    | --- | --- |
    | `fadeIn(seconds)` / `fadeInSmooth(seconds)` | 0→1 over the first `seconds` of the slide |
    | `fadeOut(seconds)` | 1→0 |
    | `pulse(attack, release)` | rises then falls |
    | `fadeInAt(kf, seconds)` / `fadeInAtSmooth(kf, seconds)` | 0 before a keyframe, then ramps |
    | `onceAt(kf)` | hard 0/1 switch at a keyframe |
    | `betweenKeyframes(from_kf, to_kf)` | 1 only between two keyframes |
    | `stageAfter(kf, count)` / `stageAfterSmooth(kf, count, seconds)` | staged reveal, `count` steps |
    | `slideAlpha()` | the deck's own intro/outro, eased |
    | `shaderTime()` | seconds since this shader appeared (does not reset per slide) |

    ```glsl
    #include <slide.glsl>

    void main() {
        vec3 col = vec3(0.2, 0.5, 0.9) * fadeInSmooth(0.6);
        if (afterKeyframe(reveal))
            col += vec3(0.8, 0.2, 0.2) * float(stageAfter(reveal, 3)) * 0.2;
        fragColor = vec4(col * slideAlpha(), 1.0);
    }
    ```

    `reveal` here is a deck keyframe name, baked in as a `#define`.

!!! info "Include path resolution"
    `#include`d files resolve against the including file first, then the project data path, then this stdlib (`Options::ShaderPath`, the `src/shaders/` directory, configurable via the `SLOPE_SHADER_PATH` cmake cache variable, installed under `share/slope/shaders` too).
