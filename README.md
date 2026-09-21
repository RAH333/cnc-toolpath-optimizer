# cnc-toolpath-optimizer
CNC Toolpath Optimizer

# CNC Toolpath & Industrial Cycle-Time Optimizer

An open-source automation tool built to parse numerical control (NC) programs, compute rigorous time studies, and safely optimize toolpath feed rates inside structural bounds configured for industrial controllers like **Siemens SINUMERIK** and **Fanuc**.

## System Architecture
The application pipeline mirrors the modular structure of industrial CAM/CNC post-processors:
1. **Config Layer (`/config`)**: Manages physical limits (maximum spindle speeds, structural maximum feed rates, rapid travel rates).
2. **Parser Layer (`parser.py`)**: Reads standard ISO industrial G-code formats, filtering comments out while isolating modal groups (G, M, T, F, S, and coordinates).
3. **Analytics Engine (`utils.py`)**: Simulates 3D linear distance vectors tracking continuous path configurations to output accurate time metrics.
4. **Optimization Pipeline (`optimizer.py`)**: Safely updates cutting performance parameters up to machine limits to reduce shop floor production bottlenecks.

## How to Run the Project
Ensure you have Python 3.x installed. Run from the root directory:

```bash
python main.py
```

## Industrial Value Delivery
- **Time Studies Framework**: Generates rapid estimation metrics for assembly lines without taking physical machine run-times.
- **Scrap & Wear Prevention**: Caps absolute program velocity profiles dynamically preventing physical tool breakage and over-travel damage.
- 

```
cnc-toolpath-optimizer/
│
├── config/
│   └── machine_profiles.json
│
├── data/
│   ├── sample_input.nc
│   └── optimized_output.nc
│
├── src/
│   ├── __init__.py
│   ├── parser.py
│   ├── optimizer.py
│   └── utils.py
│
├── main.py
├── requirements.txt
└── README.md
```
