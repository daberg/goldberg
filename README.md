# Goldberg's algorithm implementation and benchmarking in Python

Advanced algorithms and parallel computing course project

Politecnico di Milano

2018

## Browsing the repository

[**Presentation and discussion of results**](/doc.pdf)

[Python package source code](/goldberg)

## Installing and running

* **The Docker way**

  Since the graph-tool module takes a *very* long time to compile, the code is bundled with a special-purpose docker image to automatically take care of dependencies.

  Let's say we want to run a simple test script called *test.py*.

  ```shell
  # Clone repository
  git clone https://github.com/daberg/goldberg
  cd goldberg

  # Add test script
  echo "#---Some Python code that makes use of the goldberg module---#" > test.py

  # Build Docker image
  scripts/docker-build.sh

  # Run script inside Docker container
  scripts/docker-run.sh python test.py
  ```

  Notice that the test code must be inside the projects path, since it is the only path that gets mounted in the docker container.

* **The traditional way**

  * Install the graph_tool module

    Just follow the [instructions](https://git.skewed.de/count0/graph-tool/wikis/installation-instructions) (warning: can take hours, together with several GBs of RAM)

  * Install the memory_profiler module

    ```shell
    sudo pip install memory_profiler
    ```

  * Install the goldberg module

    ```shell
    git clone https://github.com/daberg/goldberg
    cd goldberg
    sudo pip install .
    ```

  * Just run any script using the module, anywhere in the filesystem
