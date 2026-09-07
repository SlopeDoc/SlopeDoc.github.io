// Demo for docs/Primitives/code.md — the Code primitive: a source listing that
// writes itself out across slide changes and lights up its named regions.

#include "slope.h"

using namespace slope;

Slideshow show;

int main(int argc, char** argv)
{
    show.init("code", argc, argv);

    auto py = Code::FromFile("newton.py");   // language read off the extension
    py->style.line_numbers = true;
    py->style.font = Code::LoadFont("FiraCode-Regular.ttf");

    Latex::AddToPrefix("\\usepackage{libertine}");
    Latex::AddToPrefix("\\usepackage{libertinust1math}");   // libertine math too

    show << Title("Walk through your algorithms!")->at(TOP);
    show << py->at("listing") << py->reveal(START);   // nothing written yet

    // written out in two steps
    show << inNextFrame << py->reveal("loop");        // up to the iteration
    show << inNextFrame << py->reveal(END);           // the rest of it

    // then walked through in three
    show << inNextFrame << py->focus(1, 5);           // the helpers f and df
    show << inNextFrame << py->focus("loop");         // the Newton step
    show << inNextFrame << py->focus("test");         // the stopping test
    show << inNextFrame << py->unfocus();             // back to rest

    show.run();
    return 0;
}
