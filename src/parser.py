import re

class GCodeParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.blocks = []

    def parse(self):
        """Parses the NC file line by line extracting modal information."""
        with open(self.filepath, 'r') as file:
            for line in file:
                cleaned = re.sub(r'\(.*?\)', '', line).strip()  # Strip comments
                if not cleaned:
                    continue
                
                block_data = self._parse_line(cleaned)
                if block_data:
                    self.blocks.append(block_data)
        return self.blocks

    def _parse_line(self, line):
        data = {'line': line}
        # Regex to find commands like G01, X10.5, F500
        matches = re.findall(r'([A-Z])([-+]?\d*\.\d+|\d+)', line)
        
        for letter, value in matches:
            if letter in ['G', 'M', 'T']:
                data[letter] = int(value)
            elif letter in ['X', 'Y', 'Z', 'F', 'S']:
                data[letter] = float(value)
        return data
      
