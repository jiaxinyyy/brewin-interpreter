# CS 131 Spring 2023: Project

Hey there! This is a repository for [CS 131](https://ucla-cs-131.github.io/spring-23/)'s quarter-long project: making an interpreter. The project specs are as follows:

1. [Project 1 Spec](https://docs.google.com/document/d/1pPQ2qZKbbsbZGBSwvuy1Ir-NZLPMgVt95WPQuI5aPho)
2. [Project 2 Spec](https://docs.google.com/document/d/1simlDMO0TK-YNDPYjkuU1C3fcaBpbIVYRaKD1pdqJj8/edit?usp=sharing)
3. [Project 3 Spec](https://docs.google.com/document/d/1YqSGkY4lE5nr-u27TQ-C8vd7f21SQA-qHL1aZf0ye4s/edit?usp=sharing)

There are three stages to the project; students are currently at the third. Thus, this folder contains the necessary bootstrapping code:

- `intbase.py`, the base class and enum definitions for the interpreter
- `bparser.py`, a static `parser` class to parse Brewin programs

- `interpreterv2.py`, a working top-level interpreter for project 2 that mostly delegates interpreting work to:
  - `classv2.py` which handles class, field, and method definitions
  - `env2.py` which handles the program environment (a stack-based approach to accommodate local variables)
  - `objectv2.py` which additional implements inheritance and method calling; most of the code is here!
  - `type_valuev2.py` which additionally manage type checking

- `interpreterv1.py`, a working top-level interpreter for project 1 that mostly delegates interpreting work to:
  - `classv1.py` which handles class, field, and method definitions
  - `env1.py` which handles the program environment (a map from variables to values)
  - `objectv1.py` which handles operations on *objects*, which include statements, expressions, etc; most of the code is here!
  - `type_valuev1.py` which has classes to create type tags

You can view the starter for [Project 1](https://github.com/UCLA-CS-131/spring-23-project-starter/releases/tag/p1).

## Licensing and Attribution

This is an unlicensed repository; even though the source code is public, it is **not** governed by an open-source license.

This code was primarily written by [Carey Nachenberg](http://careynachenberg.weebly.com/), with support from his TAs for the [Spring 2023 iteration of CS 131](https://ucla-cs-131.github.io/spring-23/).
