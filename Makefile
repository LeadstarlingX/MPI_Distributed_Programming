# Default number of processes
NP ?= 4

# Use the specific python binary found in host shell (which is 3.6.10)
PYTHON := /usr/bin/python
PYTHON_VERSION := 3.6

# Ensure user site-packages are visible for the correct version
PYTHONPATH := $(HOME)/.local/lib/python$(PYTHON_VERSION)/site-packages:$(PYTHONPATH)
export PYTHONPATH

all: p1 cpp_p2

install:
	$(PYTHON) -m pip install --user --upgrade pip
	$(PYTHON) -m pip install --user numpy
	$(PYTHON) -m pip install --user --force-reinstall --no-binary=mpi4py "mpi4py==3.1.6"

p1:
	@echo "Running Problem 1 (Prefix Sum) with NP=$(NP)..."
	@echo "Using $(PYTHON) (Version: $$($(PYTHON) --version))"
	mpiexec -n $(NP) -genv PYTHONPATH $(PYTHONPATH) $(PYTHON) src/problem1/prefix_sum.py



# Colors for terminal output
BLUE         := \033[1;34m
GREEN        := \033[1;32m
CYAN         := \033[1;36m
YELLOW       := \033[1;33m
RED          := \033[1;31m
NC           := \033[0m # No Color

# SimGrid Configuration
PLAT ?= fat_tree
N ?= 1000000
# Fixed host speed based on calibration (approx 6.4Gf for this machine)
HOST_SPEED ?= 6.43Gf

cpp_p2:
	@echo "$(BLUE)==================================================$(NC)"
	@echo "$(BLUE)  Compiling C++ Manual Reduce for SimGrid       $(NC)"
	@echo "$(BLUE)==================================================$(NC)"
	@smpicxx -O3 src/problem2/manual_reduce.cpp -o manual_reduce_cpp
	@echo "$(GREEN)Done.$(NC)"

run_sim:
	@echo "$(CYAN)➔ Simulating [$(PLAT)] Topology | Nodes: $(NP) | N: $(N)$(NC)"
	@smpirun -np $(NP) -platform platforms/$(PLAT).xml --cfg=smpi/host-speed:$(HOST_SPEED) --log=xbt_cfg.thresh:warning ./manual_reduce_cpp $(N)
	@echo ""

bench_all: cpp_p2
	@echo "$(YELLOW)🔍 Calibrating host speed once...$(NC)"
	$(eval HOST_SPEED := $(shell smpirun -np 1 -platform platforms/fat_tree.xml --cfg=smpi/host-speed:auto ./manual_reduce_cpp 1 2>&1 | grep "host-speed:" | sed 's/.*host-speed:\([0-9\.]*Gf\).*/\1/'))
	@echo "$(GREEN)✔ Calibration complete: Using $(HOST_SPEED)$(NC)"
	@echo "$(YELLOW)🚀 Comparative Benchmark: Tree vs Sequential (Gather)$(NC)"
	@echo "$(YELLOW)--------------------------------------------------------------------------------$(NC)"
	@echo "$(CYAN)Topology: Fat-Tree$(NC)"
	@$(MAKE) --no-print-directory run_sim PLAT=fat_tree NP=$(NP) N=10 HOST_SPEED=$(HOST_SPEED)
	@$(MAKE) --no-print-directory run_sim PLAT=fat_tree NP=$(NP) N=1000 HOST_SPEED=$(HOST_SPEED)
	@$(MAKE) --no-print-directory run_sim PLAT=fat_tree NP=$(NP) N=1000000 HOST_SPEED=$(HOST_SPEED)
	@echo "$(CYAN)Topology: Dragonfly$(NC)"
	@$(MAKE) --no-print-directory run_sim PLAT=dragonfly NP=$(NP) N=10 HOST_SPEED=$(HOST_SPEED)
	@$(MAKE) --no-print-directory run_sim PLAT=dragonfly NP=$(NP) N=1000 HOST_SPEED=$(HOST_SPEED)
	@$(MAKE) --no-print-directory run_sim PLAT=dragonfly NP=$(NP) N=1000000 HOST_SPEED=$(HOST_SPEED)
	@echo "$(YELLOW)--------------------------------------------------------------------------------$(NC)"
	@echo "$(GREEN)🏆 Comparative Benchmark Complete!$(NC)"

clean:
	@echo "$(RED)Cleaning up binaries and cache...$(NC)"
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete
	@rm -f manual_reduce_cpp
	@echo "$(GREEN)Cleaned.$(NC)"
