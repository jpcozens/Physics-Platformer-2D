# 2D Physics Platformer \[College Project\]

## Summary

* A project I developed in college for my non-exam-assessment.
* 2D physics platformer with 2 levels.
* Contains a level creator to create your own levels, which I used to create the levels.

While this project is definitely a mess, it was my introduction to building real programs and I learnt a lot from doing so - in many different areas, thanks to the large scope.

## If you wish to use the program

To open the program, simply clone it and run the main file from a terminal or manually.
The program is intended to be used on systems with 1920x1080 resolution, and was only ever run on a windows machine with decent specs, so expect bugs if you choose a different machine.
The physics aren't incredible and never reached a point I was happy with, so be prepared for anger if you attempt to actually beat the two levels.

## Controls + Info

* WASD to move
* left click to use the baseball bat - current only use is to detonate grenades before they collide with anything.
* right click to use the grappling hook - only attaches to wood and can pass through transparent blocks.
* space bar to jump + double jump

If you use the level creator, remember the name of the file to enter it into the custom level menu.
The accounts and online section on the main menu are not functional, so the buttons do nothing.

## Learning points from this project

This project was my entry point into building a real project with python, and as such a lot went wrong which I have since learnt from!
Here's a list of all the things I'd say I learnt from this project.

* Splitting code into multiple files is *imperative*. I knew of the existence of doing such a thing in python but was not sure how, and did not expect the file to become so large.
* Handling scope for projects is very important, I had a lot of things I wanted to do in this project, and while a lot of them did get finished, none of them were particularly produced to a good quality as I had to split the workload among many different aspects.
* Tweaking physics properties is difficult, and a lot of thought should be put into the design of the physics to make it easily editable and maintainable.
* Writing unit tests is important. While it was not required for the project since it was only a college project, it would've made my life a whole lot easier, especially considering the monster of a main file it was all contained in.
* While I did not end up including this in the final handin and have since lost the file, I learnt a lot about using network sockets for multiplayer games, including having an authoritarian server and client-side prediction.
