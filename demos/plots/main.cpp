// Demo for docs/Primitives/plots/board.md — a board is the frame; the curves
// drawn in it are functions of time (snippets.lua, re-read on save) so they
// move, and each curve is a shader you can edit (see views/pulse.glsl).

#include "slope.h"
#include <random>

using namespace slope;

Slideshow show;

int main(int argc, char** argv)
{
    show.init("board", argc, argv);
    Latex::AddToPrefix("\\usepackage{libertine}");
    Latex::AddToPrefix("\\usepackage{libertinust1math}");   // libertine math too
    Snippet::load("snippets.lua");

    auto fig = Board::Add("fig", vec2(-M_PI, M_PI), vec2(-1.3, 1.3));

    // readings of the damped wave at rest, for the scatter to sit on
    std::vector<vec2> pts;
    std::mt19937 rng(4);
    std::normal_distribution<double> noise(0, 0.08);
    for (double x = -3.0; x <= 3.0; x += 0.3) {
        const double env = std::exp(-0.2 * x * x);   // same envelope as the wave snippet
        pts.push_back(vec2(x, std::sin(2 * x) * env + noise(rng)));
    }

    auto wave = Plot::FromSnippet("wave", fig, "wave");
    wave->caption = "$\\sin(2x - \\omega t)$";

    auto pulse = Plot::FromSnippet("pulse", fig, "pulse");
    pulse->caption = "wave packet";

    auto samples = Scatter::Add("samples", fig, pts);
    samples->caption = "samples";

    // one title, added once; inNextFrame carries it forward
    show << Title("Plot the world")->at(TOP);
    show << fig->at("figure") << wave;                  // the frame, and a curve in it

    show << inNextFrame << pulse << Legend::Add(fig);   // a second curve, shader in views/pulse.glsl
    show << inNextFrame << samples;                     // the readings themselves

    show.run();
    return 0;
}
