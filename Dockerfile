FROM tiagopeixoto/graph-tool

RUN cd /opt && \
    pacman -Sy --noconfirm python-pip && \
    pip install memory_profiler
