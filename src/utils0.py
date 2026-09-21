# Utility features designed to simulate real-world shop floor time studies.
import math

def calculate_cycle_time(blocks, profile):
    """Calculates an estimated structural cycle time based on feed rates and simple linear distance."""
    total_time_min = 0.0
    current_pos = {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
    current_feed = 500.0 # Default fallback feed

    for block in blocks:
        if 'F' in block:
            current_feed = block['F']
            
        # Target coordinates
        target_x = block.get('X', current_pos['X'])
        target_y = block.get('Y', current_pos['Y'])
        target_z = block.get('Z', current_pos['Z'])
        
        # Calculate 3D linear distance traversed
        distance = math.sqrt(
            (target_x - current_pos['X'])**2 + 
            (target_y - current_pos['Y'])**2 + 
            (target_z - current_pos['Z'])**2
        )
        
        if distance > 0:
            feed_rate = profile["rapid_traverse_rate_mm_min"] if block.get('G') == 0 else current_feed
            total_time_min += distance / feed_rate
            
        current_pos.update({'X': target_x, 'Y': target_y, 'Z': target_z})
        
    return total_time_min * 60 # Return in seconds
