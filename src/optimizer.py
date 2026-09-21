import re

#class ToolpathOptimizer:
    #def __init__(self, blocks, profile):

class ToolpathOptimizer:
    def __init__(self, blocks, profile):
        self.blocks = blocks
        self.profile = profile

    def optimize_feeds(self, efficiency_multiplier=1.15):
        """
        Optimizes feed rates by safely pushing rates up to maximum machine limits
        during straight cuts while ensuring bounds safety.
        """
        optimized_blocks = []
        max_feed = self.profile["max_feed_rate_mm_min"]

        for block in self.blocks:
            opt_block = block.copy()
            # If it's a linear interpolation cutting movement (G1)
            if opt_block.get('G') == 1 and 'F' in opt_block:
                current_feed = opt_block['F']
                new_feed = min(current_feed * efficiency_multiplier, max_feed)
                opt_block['F'] = round(new_feed, 2)
                
                # Reconstruct line text
                line_text = opt_block['line']
                opt_block['line'] = re.sub(r'F\d+(\.\d+)?', f"F{opt_block['F']}", line_text)
            
            optimized_blocks.append(opt_block)
        return optimized_blocks
