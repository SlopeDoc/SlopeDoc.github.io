#include "slope.h"
#include <vector>
#include <cmath>
using namespace slope;

Slideshow show;

int main(int argc, char** argv) {
    show.init("shader_advanced", argc, argv);
    Latex::AddToPrefix("\\usepackage{libertine}");

    // ── multiple render targets ──────────────────────────────────────────
    show << Latex::Add("Multiple render targets")->at(TOP);
    auto mrt = Shader::FromFile("mrt.frag", 700, 500);
    mrt->setTargets(2);
    show << mrt->at(CENTER);

    // ── CPU -> GPU : recomputed and re-uploaded every frame ────────────────
    show << newFrame << Latex::Add("CPU $\\to$ GPU")->at(TOP);
    const int N = 64;
    std::vector<float> field(N * N);
    auto fieldShader = Shader::FromFile("field.frag", 700, 500);
    fieldShader->updater = [fieldShader, field, N](TimeObject t) mutable {
        for (int y = 0; y < N; ++y)
            for (int x = 0; x < N; ++x) {
                float dx = float(x - N / 2), dy = float(y - N / 2);
                float r = std::sqrt(dx * dx + dy * dy);
                field[y * N + x] = 0.5f + 0.5f * std::sin(r * 0.5f - float(t.inner_time) * 2.0f);
            }
        fieldShader->setTexture("source", field, N, N);
    };
    show << fieldShader->at(CENTER);

    // ── shader storage buffers : a tiny bouncing-particle simulation ──────
    show << newFrame << Latex::Add("Shader storage buffers")->at(TOP);
    const int P = 8;
    std::vector<float> particles(P * 4);   // (x, y, vx, vy) per particle
    for (int i = 0; i < P; ++i) {
        float a = float(i) / P * 6.2831853f;
        particles[i * 4 + 0] = 0.6f * std::cos(a);
        particles[i * 4 + 1] = 0.6f * std::sin(a);
        particles[i * 4 + 2] = 0.5f * std::sin(a * 2.0f + 1.0f);
        particles[i * 4 + 3] = 0.5f * std::cos(a * 3.0f);
    }
    auto compute = Shader::FromFile("compute.frag", 700, 500);
    compute->setBuffer(0, particles);
    compute->updater = [compute, particles, P](TimeObject t) mutable {
        float dt = float(t.delta_time);
        for (int i = 0; i < P; ++i) {
            float* p = &particles[i * 4];
            p[0] += p[2] * dt;
            p[1] += p[3] * dt;
            if (p[0] < -1.0f || p[0] > 1.0f) p[2] *= -1.0f;
            if (p[1] < -1.0f || p[1] > 1.0f) p[3] *= -1.0f;
        }
        compute->setBuffer(0, particles);
    };
    show << compute->at(CENTER);

    show.run();
    return 0;
}
