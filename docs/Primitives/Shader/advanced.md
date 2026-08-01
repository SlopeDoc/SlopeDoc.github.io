---
title: Advanced shader usage
---

This page described the more advanced features that could be used to implement your more advanced GPU programs for live-demos.

Passes run in the order they are streamed into the slide, `show << producer << consumer`,
and each primitive's `updater` runs right after that primitive has drawn.

## Render target

The offscreen target every pass draws into. Independent of the size the primitive is shown
at on the slide.

| Signature | Effect |
| --- | --- |
| `static ShaderPtr FromFile(const path& file, int w = 0, int h = 0)` | `w`/`h` set the render resolution; `<= 0` keeps the window's own |
| `static ShaderPtr Add(const std::string& src, int w = 0, int h = 0)` | same, from a source string |
| `void setResolution(int w, int h)` | render resolution in pixels, what `iResolution` reports |
| `int bufferWidth() const` / `int bufferHeight() const` | that resolution |
| `void setFloatBuffer(bool on = true)` | RGBA32F attachments instead of 8-bit |
| `void setFilter(Filter f)` | how this shader's own target is sampled |
| `void setWrap(Wrap w)` | `Wrap::Clamp` (default) or `Wrap::Repeat` |
| `void setHidden(bool on = true)` | keep rendering every frame, never blit onto the slide |

```c++
enum class Shader::Filter { Nearest, Linear };
enum class Shader::Wrap   { Clamp, Repeat };
```

A hidden pass still has to be streamed into the slide to run: `setHidden` suppresses the
blit, not the render. State that is integrated rather than looked at wants
`setFloatBuffer()` and `Filter::Nearest`.

## Channels

`iChannel0..3` are the pass's sampler inputs, declared by the prelude:

```glsl
uniform sampler2D iChannel0;             // .. iChannel3
uniform vec3      iChannelResolution[4]; // (w, h, 1) per channel
```

| Signature | Source bound to `iChannel`*i* |
| --- | --- |
| `void setChannel(int i, const path& image_file, Filter f = Filter::Linear, Wrap w = Wrap::Clamp)` | an image file, loaded once |
| `void setChannel(int i, const ShaderPtr& src, int attachment = 0)` | another pass's current output |
| `void setChannelSelf(int i, int attachment = 0)` | this pass's previous frame (ping-pong) |
| `void setData(int i, const float* data, int w, int h, int comps = 1, Filter f = Filter::Linear, Wrap wrap = Wrap::Clamp)` | a CPU array as a float texture |
| `void setData(int i, const std::vector<float>& data, int w, int h, int comps = 1, Filter f = Filter::Linear, Wrap wrap = Wrap::Clamp)` | same, from a vector |
| `void clearChannel(int i)` | unbind, freeing the texture if the channel owned one |

`comps` is components per texel, 1 to 4 (R, RG, RGB, RGBA), so `setData` reads
`w * h * comps` floats in row-major order. Calling it again with the same size and
component count updates the texture in place instead of recreating it, which is what makes
a per-frame upload cheap.

`setChannelSelf` allocates a second target and alternates between the two, so the shader
samples what it wrote last frame while writing the current one.

## Multiple render targets

`fragColor` is location 0 and is already declared. Extra outputs are declared explicitly,
up to four in total, and location 0 must not be redeclared:

```glsl
layout(location = 1) out vec4 oPosition;
```

| Signature | Effect |
| --- | --- |
| `void setTargets(int n)` | number of colour attachments, 1 to 4 |
| `int targets() const` | that number |

The slide always shows attachment 0. The others are reached through
`setChannel(i, src, attachment)` downstream, or `readback(out, attachment)` from the CPU.

## Storage buffers

Buffers the shader reads *and writes*, and the only way a fragment shader writes anywhere
other than its own pixel:

```glsl
layout(std430, binding = 0) buffer Density { uint density[]; };
```

| Signature | Effect |
| --- | --- |
| `void setBuffer(int binding, const void* data, std::size_t bytes)` | upload, creating the buffer if needed |
| `template<class T> void setBuffer(int binding, const std::vector<T>& v)` | same, `v.size() * sizeof(T)` bytes |
| `void allocBuffer(int binding, std::size_t bytes)` | reserve a zeroed buffer, uploading nothing |
| `bool readBuffer(int binding, void* dst, std::size_t bytes) const` | read back; `false` if there is no buffer at that binding |
| `template<class T> bool readBuffer(int binding, std::vector<T>& v) const` | same, into a vector you have already sized |
| `void clearBufferData(int binding, unsigned int value = 0)` | refill the whole buffer with `value`, GPU-side (GL 4.3; a no-op below that) |
| `void shareBuffer(int binding, const ShaderPtr& src, int src_binding)` | bind another pass's buffer here as well |
| `void clearBuffer(int binding)` | drop this binding; the allocation dies with its last holder |

Re-uploading the same byte count reuses the allocation, so a `setBuffer` per frame is a
copy and not a reallocation. A memory barrier is issued after every draw, so writes are
visible to a later pass in the same frame and to `readBuffer`.

`shareBuffer` gives two passes one allocation with no copy: the producer must be streamed
first, and the source must already hold a buffer at `src_binding`. A binding shared into a
pass is bound and readable from C++ even if that pass's GLSL never declares it.

Core GLSL has `atomicAdd`, `atomicMin`, `atomicMax`, `atomicExchange` and
`atomicCompSwap` on `uint` and `int`, but nothing on `float`, so accumulating a real
quantity means scaling it into fixed point and dividing on the way out. Size the scale so
that contributors × largest contribution × scale stays well under 2³²: an overflow is
silent.

## Readback

| Signature | Returns |
| --- | --- |
| `bool readback(std::vector<float>& out, int attachment = 0) const` | the whole attachment, 4 floats per texel, row-major, bottom-up. `false` if nothing has been rendered yet |
| `RGBA readbackMean(int attachment = 0) const` | the mean over the attachment |
| `RGBA readbackPixel(int x, int y, int attachment = 0) const` | one texel |

An 8-bit target comes back normalised to 0..1, a float target exact. All three are
synchronous: the call returns only once the GPU has caught up, and that stall, not the byte
count, is what a per-frame readback costs. Reducing on the GPU and reading a handful of
bytes out of a buffer is the cheap alternative, which is what the example below does.

An `updater` runs after its pass has drawn, so a readback there sees the frame that was
just rendered.

## Full example

Everything above in one program: a 65536-particle simulation living in a float texture,
scattering itself into a shared density grid with atomics, coloured by a second pass, with
the peak density reduced on the GPU and read back as four bytes to normalise the display.

=== "main.cpp"

    ```c++ title="main.cpp"
    #include "slope.h"
    #include <vector>
    #include <cmath>
    using namespace slope;

    Slideshow show;

    constexpr int   N    = 256;     // N*N particles, one texel each
    constexpr int   GRID = 128;     // density grid, GRID*GRID cells
    constexpr int   M    = 64;      // the CPU field's resolution
    constexpr float FIX  = 4096.0f; // fixed-point scale, shared with the shaders

    int main(int argc, char** argv) {
        show.init("shader_io", argc, argv);

        // a field computed on the CPU, uploaded once as a data texture
        std::vector<float> weight(M * M);
        for (int y = 0; y < M; ++y)
            for (int x = 0; x < M; ++x) {
                float dx = (x + 0.5f) / M * 2.f - 1.f;
                float dy = (y + 0.5f) / M * 2.f - 1.f;
                weight[y * M + x] = std::exp(-6.f * (dx * dx + dy * dy));
            }

        // pass 1 : the simulation, compute only
        auto sim = Shader::FromFile("sim.frag", N, N);
        sim->setFloatBuffer();                    // state, not colour
        sim->setFilter(Shader::Filter::Nearest);  // a texel is a particle
        sim->setChannelSelf(0);                   // iChannel0 = last frame's state
        sim->setData(1, weight, M, M);            // iChannel1 = the CPU field
        sim->setHidden();
        sim->allocBuffer(0, GRID * GRID * sizeof(unsigned));   // density grid
        sim->allocBuffer(1, sizeof(unsigned));                 // peak density
        sim->set("uAttract", 0.35f);

        // pass 2 : the view, reading what pass 1 filled
        auto view = Shader::FromFile("view.frag", 900, 900);
        view->shareBuffer(0, sim, 0);   // one grid, two passes, no copy
        view->shareBuffer(1, sim, 1);   // read from C++ below, never declared in view.frag

        float peak = 1.f;
        view->bind("uPeak", [&peak] { return peak; });

        // last updater of the frame : read the reduction, then zero both
        // accumulators for the next one
        view->updater = [view, &peak](TimeObject) {
            unsigned raw = 0;
            view->readBuffer(1, &raw, sizeof(raw));            // 4 bytes across the bus
            peak = 0.95f * peak + 0.05f * std::max(1.f, float(raw) / FIX);
            view->clearBufferData(0);
            view->clearBufferData(1);
        };

        show << sim << view->at(CENTER);   // producer first
        show.run();
        return 0;
    }
    ```

=== "sim.frag"

    ```glsl title="sim.frag"
    // one texel = one particle : rg = position, ba = velocity
    layout(std430, binding = 0) buffer Density { uint density[]; };
    layout(std430, binding = 1) buffer Peak    { uint peak[]; };

    uniform float uAttract;

    const float DT   = 0.008;
    const float FIX  = 4096.0;
    const int   GRID = 128;

    float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }

    void main() {
        ivec2 id = ivec2(gl_FragCoord.xy);
        vec4 s = texelFetch(iChannel0, id, 0);
        vec2 p = s.xy, v = s.zw;

        if (iFrame < 1) {                     // seeded here, nothing uploaded at startup
            float a = 6.2831853 * hash(vec2(id));
            float r = 0.25 + 0.55 * hash(vec2(id) + 7.0);
            p = r * vec2(cos(a), sin(a));
            v = 0.9 * sqrt(r) * vec2(-sin(a), cos(a));
        }

        float w = texture(iChannel1, p * 0.5 + 0.5).r;   // the CPU field
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
    ```

=== "view.frag"

    ```glsl title="view.frag"
    #include <colormap.glsl>

    layout(std430, binding = 0) buffer Density { uint density[]; };

    uniform float uPeak;

    const float FIX  = 4096.0;
    const int   GRID = 128;

    void main() {
        vec2 uv = gl_FragCoord.xy / iResolution;
        ivec2 cell = clamp(ivec2(uv * float(GRID)), ivec2(0), ivec2(GRID - 1));
        float d = float(density[cell.y * GRID + cell.x]) / FIX;
        fragColor = vec4(inferno(clamp(d / uPeak, 0.0, 1.0)), 1.0);
    }
    ```

Reading the frame order once makes the rest fall out. Per frame: `sim` draws (scatters into
the grid, writes the new state), `view` draws (reads the grid), `view`'s updater runs
(reads the peak, zeroes both buffers for the next frame). Zeroing from `view` rather than
from `sim` is deliberate: `sim`'s updater would run before `view` had drawn, and would
hand it an empty grid.
