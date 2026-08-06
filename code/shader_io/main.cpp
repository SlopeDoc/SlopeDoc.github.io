#include "slope.h"
#include <vector>
#include <cmath>
#include <algorithm>
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
    sim->setTextureSelf("state");             // last frame's state
    sim->setTexture("field", weight, M, M);   // the CPU field
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
