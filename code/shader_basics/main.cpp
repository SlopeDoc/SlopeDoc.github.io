#include "slope.h"
using namespace slope;

Slideshow show;

int main(int argc, char** argv) {
    show.init("shader_basics", argc, argv);
    Latex::AddToPrefix("\\usepackage{libertine}");

    show << Latex::Add("Shader basics")->at(TOP);
    show << Shader::FromFile("plasma.frag", 900, 600)->at(CENTER);

    show.run();
    return 0;
}
