---
title: Transforms
---
The object to scene transform can be set with:
``` c++ 
    
    auto M = Mesh::Add("bunny.obj");
    M->localTransform = Transform::ScalePositionRotate(...);
```

Each object transform can be controled on each slide with the ```at``` method:
``` c++ 
    show << M->at(vec(1,1,1)) // same as at(Transform::Translation(x));
    show << inNextFrame << M->at(vec(-1,-1,-1)); // will transition between transforms
```

### Persistent transform and live editing

Just as for [Persistent 2D positions](../../placement/persistant_placement), setting a label allows to modify the transform in live:
```
    show << M->("bunny");
```
by pressing ```t```.


### Builders

!!! note "```Transform Translation(const vec& x)```"
!!! note "```Transform AxisAngle(scalar th, vec x)```"
!!! note "```Transform Scale(const vec& x)```"
!!! note "```Transform Scale(scalar s)```"
!!! note "```Transform ScalePositionRotate(const vec& s,const vec& p,vec axis,scalar th)```"
!!! note "```Transform ScalePositionRotate(const vec& s,const vec& p,const mat& R) ```"
     
