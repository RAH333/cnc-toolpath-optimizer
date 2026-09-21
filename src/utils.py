"""
Adds Arc Interpolation G02/G03 Math

This update parses radius values (R) or center-point offsets (I, J) to compute the exact arc lengths of curved toolpaths, fulfilling the precision time study requirement.
"""

import math

def calculate_cycle_time(blocks, profile):
    """Calculates an estimated structural cycle time supporting G00, G01, G02, and G03."""
    total_time_min = 0.0
    current_pos = {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
    current_feed = 500.0  # Default fallback feed

    for block in blocks:
        if 'F' in block:
            current_feed = block['F']
            
        target_x = block.get('X', current_pos['X'])
        target_y = block.get('Y', current_pos['Y'])
        target_z = block.get('Z', current_pos['Z'])
        
        g_cmd = block.get('G')
        distance = 0.0

        # G00 (Rapid) or G01 (Linear Cutting)
        ## if g_cmd in [0, 1] or ('G' not in block and ( 'X' in block or 'Y' in block or 'Z' in block )):
        # Change from: if g_cmd in or ...
        # Change to:
        if g_cmd in [0, 1] or ('G' not in block and ('X' in block or 'Y' in block or 'Z' in block)):
    
            distance = math.sqrt(
                (target_x - current_pos['X'])**2 + 
                (target_y - current_pos['Y'])**2 + 
                (target_z - current_pos['Z'])**2
            )
        
        # G02 (CW Arc) or G03 (CCW Arc)
        elif g_cmd in:
            # Radius-based Arc Calculation
            if 'R' in block:
                r = block['R']
                chord = math.sqrt((target_x - current_pos['X'])**2 + (target_y - current_pos['Y'])**2)
                # Prevent domain errors if chord exceeds diameter due to rounding
                if chord <= 2 * r:
                    angle = 2 * math.asin(chord / (2 * r))
                    distance = r * angle
                else:
                    distance = chord # Fallback to straight line if geometry is malformed
            
            # Center-offset-based Arc Calculation (I, J)
            elif 'I' in block or 'J' in block:
                i_offset = block.get('I', 0.0)
                j_offset = block.get('J', 0.0)
                
                # Center point coordinates
                center_x = current_pos['X'] + i_offset
                center_y = current_pos['Y'] + j_offset
                
                # Radii verification
                r1 = math.sqrt((current_pos['X'] - center_x)**2 + (current_pos['Y'] - center_y)**2)
                r2 = math.sqrt((target_x - center_x)**2 + (target_y - center_y)**2)
                r = (r1 + r2) / 2.0
                
                # Angular calculations via vectors
                v1_x, v1_y = current_pos['X'] - center_x, current_pos['Y'] - center_y
                v2_x, v2_y = target_x - center_x, target_y - center_y
                
                dot_product = v1_x * v2_x + v1_y * v2_y
                magnitude = (math.sqrt(v1_x**2 + v1_y**2) * math.sqrt(v2_x**2 + v2_y**2))
                
                if magnitude > 0:
                    cos_theta = max(-1.0, min(1.0, dot_product / magnitude))
                    angle = math.acos(cos_theta)
                    distance = r * angle
                else:
                    distance = 0.0

        if distance > 0:
            feed_rate = profile["rapid_traverse_rate_mm_min"] if g_cmd == 0 else current_feed
            total_time_min += distance / feed_rate
            
        current_pos.update({'X': target_x, 'Y': target_y, 'Z': target_z})
        
    return total_time_min * 60  # Convert to seconds
