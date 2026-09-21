"""
Adds the Visual TUI Dashboard Layout

This update creates a clean terminal frame utilizing explicit Unicode blocks and terminal formatting colors to render a real-time summary block.
"""

import json
import os
from src.parser import GCodeParser
from src.optimizer import ToolpathOptimizer
from src.utils import calculate_cycle_time

def print_dashboard(initial_time, optimized_time, machine_name):
    """Renders a responsive, clean industrial terminal status dashboard."""
    time_saved = initial_time - optimized_time
    pct_saved = (time_saved / initial_time) * 100 if initial_time > 0 else 0
    
    # ANSI escape colors
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

    print("\n" + CYAN + "╔══════════════════════════════════════════════════════════════════════╗" + RESET)
    print(CYAN + "║ " + BOLD + "    SIEMENS ENERGY - AUTOMATED CNC CYCLE OPTIMIZATION ENGINE      " + RESET + CYAN + " ║" + RESET)
    print(CYAN + "╠══════════════════════════════════════════════════════════════════════╣" + RESET)
    print(CYAN + "║" + RESET + f" Target Controller Profile : {YELLOW}{machine_name.upper():<39}{RESET}" + CYAN + "║" + RESET)
    print(CYAN + "║" + RESET + f" Toolpath Interpolation   : {GREEN}{'ENABLED (G00, G01, G02, G03)':<39}{RESET}" + CYAN + "║" + RESET)
    print(CYAN + "╠══════════════════════════════════════════════════════════════════════╣" + RESET)
    print(CYAN + "║ " + BOLD + "PRODUCTION PERFORMANCE METRICS:" + RESET + "                                     " + CYAN + "║" + RESET)
    print(CYAN + "║" + RESET + f"  • Baseline Cycle Time   : {initial_time:.2f} seconds                      " + CYAN + "║" + RESET)
    print(CYAN + "║" + RESET + f"  • Optimized Cycle Time  : {optimized_time:.2f} seconds                      " + CYAN + "║" + RESET)
    print(CYAN + "║" + RESET + f"  • Net Factory Savings   : {GREEN}{time_saved:.2f} seconds ({pct_saved:.1f}% Efficiency) {RESET:<10}" + CYAN + "║" + RESET)
    print(CYAN + "╚══════════════════════════════════════════════════════════════════════╝\n")

def main():
    # Load Controller Profiles
    with open('config/machine_profiles.json', 'r') as f:
        profiles = json.load(f)
    machine_name = 'siemens_840d'
    siemens_profile = profiles[machine_name]

    input_file = 'data/sample_input.nc'
    output_file = 'data/optimized_output.nc'

    # Parsing Execution
    parser = GCodeParser(input_file)
    raw_blocks = parser.parse()

    # Metrics computation
    initial_time = calculate_cycle_time(raw_blocks, siemens_profile)

    # Optimization pipeline execution
    optimizer = ToolpathOptimizer(raw_blocks, siemens_profile)
    optimized_blocks = optimizer.optimize_feeds(efficiency_multiplier=1.25)

    # Save output to build optimized file
    with open(output_file, 'w') as out:
        for block in optimized_blocks:
            out.write(block['line'] + '\n')

    optimized_time = calculate_cycle_time(optimized_blocks, siemens_profile)
    
    # Print beautiful dashboard output
    print_dashboard(initial_time, optimized_time, machine_name)

if __name__ == "__main__":
    main()
  
