# Enhanced Fleet Plots
# This script generates enhanced plots for fleet size changes on the ridehail market.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

def setup_plot_style():
    """Set up the base plotting style"""
    plt.style.use('default')
    sns.set_style("whitegrid")
    
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['axes.linewidth'] = 1.5

def prepare_data(constant_price):
    """Prepare data by calculating percentage differences"""
    # Calculate percentage differences for mode shares
    constant_price['rh_solo_share_pc_diff'] = ((constant_price['Trip Exec Share Ride Hail'] - 
                                               constant_price['Trip Exec Share Ride Hail'].iloc[1]) / 
                                              constant_price['Trip Exec Share Ride Hail'].iloc[1])
    
    constant_price['rh_pooled_share_pc_diff'] = ((constant_price['Trip Exec Share Ride Hail Pooled'] - 
                                                 constant_price['Trip Exec Share Ride Hail Pooled'].iloc[1]) / 
                                                constant_price['Trip Exec Share Ride Hail Pooled'].iloc[1])
    
    # Filter data for fleet size < 5
    return constant_price[constant_price['Total fleet size'] < 5]

def create_combined_plot(df_joint, constant_price_prepared, n_fleets_1=2, price_rh_solo=1, price_rh_pooled=1):
    """Create a single figure with both plots side by side"""
    setup_plot_style()
    
    # Create figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 8))
    
    # Color palette with better contrast
    colors = ['#2E86C1', '#E67E22']  # Deep blue and warm orange
    
    # Plot 1: Wait Times
    # Plot RH solo data
    sns.lineplot(
        data=df_joint.loc[(df_joint['n_fleets'] == n_fleets_1) & 
                         (df_joint['Type'] == 'RH solo') & 
                         (df_joint['price_solo'] == price_rh_solo) & 
                         (df_joint['price_pooled'] == price_rh_pooled)],
        x="size",
        y="pc_diff",
        marker='o',
        markersize=10,
        color=colors[0],
        linewidth=2.5,
        label=f"RH Solo, {n_fleets_1} fleets",
        ax=ax1
    )
    
    # Plot RH pooled data
    sns.lineplot(
        data=df_joint.loc[(df_joint['n_fleets'] == n_fleets_1) & 
                         (df_joint['Type'] == 'RH pooled') &
                         (df_joint['price_solo'] == price_rh_solo) & 
                         (df_joint['price_pooled'] == price_rh_pooled)],
        x="size",
        y="pc_diff",
        marker='s',
        markersize=10,
        color=colors[1],
        linewidth=2.5,
        linestyle='--',
        label=f'RH Pooled, {n_fleets_1} fleets',
        ax=ax1
    )
    
    # Plot 2: Mode Shares
    sns.lineplot(
        data=constant_price_prepared.loc[(constant_price_prepared['Number of fleets'] == n_fleets_1) & 
                                       (constant_price_prepared['RH Solo Price'] == price_rh_solo) & 
                                       (constant_price_prepared['RH Pooled Price'] == price_rh_pooled)],
        x="Total fleet size",
        y='rh_solo_share_pc_diff',
        marker='o',
        markersize=10,
        color=colors[0],
        linewidth=2.5,
        label=f"RH Solo, {n_fleets_1} fleets",
        ax=ax2
    )
    
    sns.lineplot(
        data=constant_price_prepared.loc[(constant_price_prepared['Number of fleets'] == n_fleets_1) &
                                       (constant_price_prepared['RH Solo Price'] == price_rh_solo) & 
                                       (constant_price_prepared['RH Pooled Price'] == price_rh_pooled)],
        x="Total fleet size",
        y='rh_pooled_share_pc_diff',
        marker='s',
        markersize=10,
        color=colors[1],
        linewidth=2.5,
        linestyle='--',
        label=f'RH Pooled, {n_fleets_1} fleets',
        ax=ax2
    )
    
    # Customize both plots
    for ax in [ax1, ax2]:
        ax.set_xticks([1.0, 1.64, 2.0, 3.0, 4.0])
        ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.0%}'))
        ax.xaxis.set_major_formatter(StrMethodFormatter('{x:,.0%}'))
        ax.legend(bbox_to_anchor=(0.5, 1.15), 
                 loc='center', 
                 ncol=2,
                 frameon=True,
                 fancybox=True,
                 shadow=True)
        
    # Set labels for first plot
    ax1.set_ylabel('Median Evening Peak Wait Time\nChange from Baseline (%)', 
                  fontsize=14, 
                  fontweight='bold',
                  labelpad=15)
    ax1.set_xlabel('Total Fleet Size\n(Relative to Baseline)', 
                  fontsize=14, 
                  fontweight='bold',
                  labelpad=15)
    
    # Set labels for second plot
    ax2.set_ylabel('Mode Share\nChange from Baseline (%)', 
                  fontsize=14, 
                  fontweight='bold',
                  labelpad=15)
    ax2.set_xlabel('Total Fleet Size\n(Relative to Baseline)', 
                  fontsize=14, 
                  fontweight='bold',
                  labelpad=15)
    
    # Add subplot labels
    ax1.text(-0.1, 1.1, '(a)', transform=ax1.transAxes, fontsize=16, fontweight='bold')
    ax2.text(-0.1, 1.1, '(b)', transform=ax2.transAxes, fontsize=16, fontweight='bold')
    
    # Adjust layout
    plt.tight_layout()
    
    return fig

def save_combined_plot(df_joint, constant_price):
    """Save the combined plot"""
    # Prepare the data
    constant_price_prepared = prepare_data(constant_price)
    
    # Create and save combined plot
    combined_fig = create_combined_plot(df_joint, constant_price_prepared)
    combined_fig.savefig('combined_plots_enhanced.eps', 
                        bbox_inches='tight', 
                        dpi=300)
    plt.close(combined_fig)

if __name__ == "__main__":
    # Load data
    df_joint = pd.read_csv('df_joint.csv')
    constant_price = pd.read_csv('constant_price.csv')
    
    # Create and save combined plot
    save_combined_plot(df_joint, constant_price)
