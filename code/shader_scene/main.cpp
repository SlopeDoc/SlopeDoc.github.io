#include "slope.h"
using namespace slope;

Slideshow show;

int main(int argc, char** argv) {
    show.init("shader_scene", argc, argv);
    Latex::AddToPrefix("\\usepackage{libertine}");

    show << Latex::Add("Registered \\& occluded")->at(TOP);
    show << Mesh::Add("spot.obj");
    show << Shader::FromFile("occluded.frag")->at(CENTER);

    show.run();
    return 0;
}
