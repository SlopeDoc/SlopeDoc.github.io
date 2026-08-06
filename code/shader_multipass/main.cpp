#include "slope.h"
using namespace slope;

Slideshow show;

int main(int argc, char** argv) {
    show.init("shader_multipass", argc, argv);
    Latex::AddToPrefix("\\usepackage{libertine}");

    show << Latex::Add("Multi-pass \\& feedback")->at(TOP);

    auto sim = Shader::FromFile("sim.frag");
    sim->setTextureSelf("previous");   // its own previous frame
    sim->setHidden();               // compute-only, feeds view below

    auto view = Shader::FromFile("colorize.frag", 700, 700);
    view->setTexture("field", sim);    // sim's output

    show << sim << view->at(CENTER);   // sim first: it feeds view

    show.run();
    return 0;
}
