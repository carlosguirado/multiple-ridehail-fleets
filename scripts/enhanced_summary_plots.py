# Enhanced Summary Plots
# This script generates enhanced summary plots for ridehail mode shares and price changes.

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter, FixedLocator, FuncFormatter

# Plot styling constants
PLOT_STYLES = {
    'colors': {
        'solo': {
            'size1': '#1f77b4',     # darker blue
            'size2': '#9ecae1',      # lighter blue
            'size4': '#08519c'       # darkest blue
        },
        'pooled': {
            'size1': '#ff7f0e',     # darker orange
            'size2': '#ffbb78',      # lighter orange
            'size4': '#d94801'       # darkest orange
        }
    },
    'font_size': 12,
    'figsize': (10, 6),
    'dpi': 100,
    'markers': {
        '1': 'o',    # circle
        '2': 's',    # square
        '4': '^'     # triangle
    },
    'lines': {
        '1': '-',     # solid
        '2': (0, (5, 5)),    # dashed with longer segments
        '4': ':'      # dotted
    }
}

def create_ridehail_plots(df):
    """Create bar plots for solo and pooled ridehail metrics"""
    # Set up plot style
    plt.rcParams['font.size'] = PLOT_STYLES['font_size']
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'
    
    # Create figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=PLOT_STYLES['dpi'])
    
    # Metrics to plot (excluding Average wait time)
    metrics = [
        'Planned mode share',
        'Executed mode share',
        'Executed rate',
        'Replanned rate'
    ]
    
    # Filter data to include only the metrics we want to plot
    plot_data = df.loc[metrics]
    
    # Set x positions for bars
    x = range(len(metrics))
    width = 0.35
    
    # Plot Solo Ridehail (left subplot)
    bars1 = ax1.bar([i - width/2 for i in x], plot_data['Solo (size: 1)'], width, 
                    label='Solo (size: 1)', color=PLOT_STYLES['colors']['solo']['size1'])
    bars2 = ax1.bar([i + width/2 for i in x], plot_data['Solo (size: 2)'], width,
                    label='Solo (size: 2)', color=PLOT_STYLES['colors']['solo']['size2'])
    
    # Plot Pooled Ridehail (right subplot)
    bars3 = ax2.bar([i - width/2 for i in x], plot_data['Pooled (size: 1)'], width,
                    label='Pooled (size: 1)', color=PLOT_STYLES['colors']['pooled']['size1'])
    bars4 = ax2.bar([i + width/2 for i in x], plot_data['Pooled (size: 2)'], width,
                    label='Pooled (size: 2)', color=PLOT_STYLES['colors']['pooled']['size2'])
    
    # Customize both subplots
    for ax, title in zip([ax1, ax2], ['(a) Solo Ridehail', '(b) Pooled Ridehail']):
        ax.set_ylabel('Percent change when moving\nfrom 2 fleets to 5 fleets')
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(metrics, rotation=45, ha='right')
        ax.grid(True, axis='y')
        ax.yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}%'))
        ax.set_ylim(-15, 20)  # Set y-axis limits based on the data
        ax.legend()
        
        # Add horizontal line at y=0
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    return fig

def format_price(x, p):
    """Custom formatter for price multiplier values"""
    if x == 0.0625:
        return "0.06"
    elif x == 0.125:
        return "0.13"
    elif x == 0.27:
        return "0.27"
    elif x == 0.47:
        return "0.47"
    else:
        return "1.00"

def create_mode_share_plot(df):
    """Create line plot showing mode share changes across price multipliers"""
    # Set up plot style
    plt.rcParams['font.size'] = PLOT_STYLES['font_size']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6), dpi=PLOT_STYLES['dpi'])
    
    # Price multipliers and corresponding column prefixes
    prices = ['1', '.47', '.27', '.125', '.0625']
    fleet_sizes = ['1', '2', '4']
    
    changes = {
        'solo_1': [], 'solo_2': [], 'solo_4': [],
        'pooled_1': [], 'pooled_2': [], 'pooled_4': []
    }
    
    # Calculate changes for each fleet size relative to price=1 baseline
    baseline_price = '1'
    for size in fleet_sizes:
        # Get baseline values at price=1
        baseline_col = f'5Fl {baseline_price}Pr {size}Flz'
        baseline_total = (df.loc['Trip Exec Ride Hail', baseline_col] + 
                         df.loc['Trip Exec Ride Hail Pooled', baseline_col])
        baseline_solo = df.loc['Trip Exec Ride Hail', baseline_col]
        baseline_pooled = df.loc['Trip Exec Ride Hail Pooled', baseline_col]
        
        for price in prices:
            col = f'5Fl {price}Pr {size}Flz'
            
            # Calculate total executed trips for this price point
            total_trips = (df.loc['Trip Exec Ride Hail', col] + 
                          df.loc['Trip Exec Ride Hail Pooled', col])
            
            # Solo change
            solo_val = df.loc['Trip Exec Ride Hail', col]
            solo_change = ((solo_val - baseline_solo) / baseline_solo) * 100
            changes[f'solo_{size}'].append(solo_change)
            
            # Pooled change
            pooled_val = df.loc['Trip Exec Ride Hail Pooled', col]
            pooled_change = ((pooled_val - baseline_pooled) / baseline_pooled) * 100
            changes[f'pooled_{size}'].append(pooled_change)
    
    # Convert price strings to floats for x-axis
    x_values = [float(p) if p != '.0625' else 0.06 for p in prices][::-1]
    
    # Plot lines
    for size in fleet_sizes:
        # Solo lines
        plt.plot(x_values, changes[f'solo_{size}'][::-1], 
                marker=PLOT_STYLES['markers'][size],
                linestyle=PLOT_STYLES['lines'][size],
                color=PLOT_STYLES['colors']['solo'][f'size{size}'],
                label=f'RH solo, size: {size}', 
                linewidth=2,
                markersize=6)
        
        # Pooled lines
        plt.plot(x_values, changes[f'pooled_{size}'][::-1],
                marker=PLOT_STYLES['markers'][size],
                linestyle=PLOT_STYLES['lines'][size],
                color=PLOT_STYLES['colors']['pooled'][f'size{size}'],
                label=f'RH pooled, size: {size}',
                linewidth=2,
                markersize=6)
    
    # Customize plot
    plt.xlabel('Price multiplier')
    plt.ylabel('Percent change in executed mode share\nfrom baseline price rate')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend(loc='upper right', frameon=True)
    
    # Set axis limits and format
    plt.xlim(0.05, 1.05)
    plt.ylim(-40, 60)
    ax.yaxis.set_major_formatter(StrMethodFormatter('{x:.0f}%'))
    
    # Set specific x-axis ticks with custom formatter
    ax.xaxis.set_major_locator(FixedLocator([0.06, 0.125, 0.27, 0.47, 1.00]))
    ax.xaxis.set_major_formatter(FuncFormatter(format_price))
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    # Read the summary subset table
    df_summary = pd.read_csv('summary_subset_table.csv', index_col=0)
    
    # Create and save the ridehail plots
    fig_ridehail = create_ridehail_plots(df_summary)
    fig_ridehail.savefig('combined_plots_enhanced.pdf', bbox_inches='tight', format='pdf')
    fig_ridehail.savefig('combined_plots_enhanced.eps', bbox_inches='tight', format='eps')
    plt.close(fig_ridehail)
    
    # Read the price comparison table for mode share plot
    df_price_comparison = pd.read_csv('price_comparison_table.csv', index_col=0)
    
    # Create and save the mode share plot
    fig_mode_share = create_mode_share_plot(df_price_comparison)
    fig_mode_share.savefig('mode_shares_by_fleet_size.eps', bbox_inches='tight', format='eps')
    plt.close(fig_mode_share)
