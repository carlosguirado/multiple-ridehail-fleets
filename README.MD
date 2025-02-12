# Multiple Ridehail Fleets Analysis

This repository contains the analysis code supporting the paper "". The codebase processes and analyzes data related to multiple ridehail fleet configurations, examining their impacts on wait times, mode shares, and distributional effects.

## Project Structure

### Python Scripts

#### `scripts/analyze_results.py`
**Inputs:**
- Raw simulation data containing fleet metrics
- Baseline and comparison scenario data

**Outputs:**
- Processed analysis of fleet size impacts
- Percentage changes in key metrics (wait times, mode shares)
- Comparative analysis between different fleet configurations

#### `scripts/enhanced_summary_plots.py`
**Inputs:**
- Processed data from analyze_results.py
- Configuration parameters for visualization

**Outputs:**
- Bar plots comparing solo and pooled ridehail metrics
- Visualization of percentage changes between different fleet sizes

#### `scripts/enhanced_fleet_plots.py`
**Inputs:**
- Processed fleet performance data
- Style configurations for plots

**Outputs:**
- Enhanced visualizations of fleet size impacts
- Styled and formatted plots for publication

### Jupyter Notebooks

#### `notebooks/INEXUS_Plots.ipynb`
**Inputs:**
- Processed data containing income deciles and mode shares
- Fleet configuration data
- Price multiplier information

**Outputs:**
- Lorenz curve visualizations
- Mode share analysis plots by income group
- SVG and PNG format plots for publication

#### `notebooks/Wait_ModeShares_Plots.ipynb`
**Inputs:**
- Wait time data for solo and pooled rides
- Mode share data across different scenarios
- Price impact data

**Outputs:**
- Comparative wait time plots
- Mode share analysis visualizations
- Price impact analysis plots
- EPS format plots for publication

## Setup and Usage

1. Clone the repository:

```bash
git clone https://github.com/yourusername/multiple-ridehail-fleets.git
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the analysis scripts in the following order:
   - First run `analyze_results.py` to process the raw data
   - Then run the plotting scripts or notebooks to generate visualizations

## Data Requirements

The analysis expects input data with the following key metrics:
- Fleet sizes and configurations
- Wait times for solo and pooled rides
- Mode shares across different scenarios
- Price multipliers
- Income decile information

## Output Files

The analysis generates several types of visualization outputs:
- SVG files for web and presentation use
- PNG files for quick viewing
- EPS files for publication
- Data summary CSV files


## License


## Authors



## Acknowledgments


