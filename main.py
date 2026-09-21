# The absolute entry-point connecting everything together.
import json
import os
from src.parser import GCodeParser
from src.optimizer import ToolpathOptimizer
from src.utils import calculate_cycle_time

def main():
    # Load Controller Profiles
    with open('config/machine_profiles.json', 'r') as f:
        profiles = json.load(f)
    siemens_profile = profiles['siemens_840d']

    input_file = 'data/sample_input.nc'
    output_file = 'data/optimized_output.nc'

    print(" [CNC Engine] Initializing Parsing Strategy...")
    parser = GCodeParser(input_file)
    raw_blocks = parser.parse()

    # Base Time Metrics
    initial_time = calculate_cycle_time(raw_blocks, siemens_profile)
    print(f" Baseline Cycle Time Estimate: {initial_time:.2f} seconds")

    # Optimization Step
    print(" [CNC Engine] Optimizing Toolpath Profiles against SIEMENS 840D limits...")
    optimizer = ToolpathOptimizer(raw_blocks, siemens_profile)
    optimized_blocks = optimizer.optimize_feeds(efficiency_multiplier=1.20)

    # Save Results
    with open(output_file, 'w') as out:
        for block in optimized_blocks:
            out.write(block['line'] + '\n')

    optimized_time = calculate_cycle_time(optimized_blocks, siemens_profile)
    time_saved = initial_time - optimized_time
    
    print(f" Optimization Complete. New Cycle Time: {optimized_time:.2f} seconds")
    print(f" Total Time Reduction: {time_saved:.2f} seconds (Saved {((time_saved/initial_time)*100):.1f}%)")

if __name__ == "__main__":
    main()
  
