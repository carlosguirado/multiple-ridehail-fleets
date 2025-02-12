# This script provides a summary of the impacts of fleet size changes on the ridehail market.
# It calculates the percentage change in mode shares, wait times, energy consumption, average speed, and VMT for 2x and 4x fleet sizes relative to the baseline scenario.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import StrMethodFormatter

def calculate_percentage_change(baseline, new_value):
    """Calculate percentage change between baseline and new value"""
    return ((new_value - baseline) / baseline) * 100

def analyze_fleet_impacts(data):
    """Analyze impacts of fleet size changes"""
    
    # Get baseline values
    baseline = data['Baseline']
    
    # Find 2x and 4x fleet columns
    fleet_2x = data['2Fl 1Pr 2Flz']  # 2x fleet size
    fleet_4x = data['2Fl 1Pr 4Flz']  # 4x fleet size
    
    results = {
        '2x_fleet': {},
        '4x_fleet': {}
    }
    
    # Analyze 2x fleet impacts
    results['2x_fleet'].update({
        # Mode shares
        'pooled_ridehail_share': {
            'baseline': baseline['Trip Mode Share Ride Hail Pooled'],
            'new': fleet_2x['Trip Mode Share Ride Hail Pooled'],
            'change': calculate_percentage_change(
                baseline['Trip Mode Share Ride Hail Pooled'],
                fleet_2x['Trip Mode Share Ride Hail Pooled']
            )
        },
        'solo_ridehail_share': {
            'baseline': baseline['Trip Mode Share Ride Hail'],
            'new': fleet_2x['Trip Mode Share Ride Hail'],
            'change': calculate_percentage_change(
                baseline['Trip Mode Share Ride Hail'],
                fleet_2x['Trip Mode Share Ride Hail']
            )
        },
        
        # Wait times
        'pooled_wait_time': {
            'baseline': baseline['AV Waiting Time RH Pooled'],
            'new': fleet_2x['AV Waiting Time RH Pooled'],
            'change': calculate_percentage_change(
                baseline['AV Waiting Time RH Pooled'],
                fleet_2x['AV Waiting Time RH Pooled']
            )
        },
        'solo_wait_time': {
            'baseline': baseline['AV Waiting Time RH Single'],
            'new': fleet_2x['AV Waiting Time RH Single'],
            'change': calculate_percentage_change(
                baseline['AV Waiting Time RH Single'],
                fleet_2x['AV Waiting Time RH Single']
            )
        },
        
        # Environmental impacts
        'energy_consumption': {
            'baseline': baseline['Energy VehicleSUM [GJ]'],
            'new': fleet_2x['Energy VehicleSUM [GJ]'],
            'change': calculate_percentage_change(
                baseline['Energy VehicleSUM [GJ]'],
                fleet_2x['Energy VehicleSUM [GJ]']
            )
        },
        'average_speed': {
            'baseline': baseline['Speed VehicleSUM [km/h]'],
            'new': fleet_2x['Speed VehicleSUM [km/h]'],
            'change': calculate_percentage_change(
                baseline['Speed VehicleSUM [km/h]'],
                fleet_2x['Speed VehicleSUM [km/h]']
            )
        },
        'total_vmt': {
            'baseline': baseline['Length VehicleSUM [km]'],
            'new': fleet_2x['Length VehicleSUM [km]'],
            'change': calculate_percentage_change(
                baseline['Length VehicleSUM [km]'],
                fleet_2x['Length VehicleSUM [km]']
            )
        },
        'deadheading_vmt': {
            'baseline': baseline['Length Vehicle SUM Empty Ride Hail [km]'],
            'new': fleet_2x['Length Vehicle SUM Empty Ride Hail [km]'],
            'change': calculate_percentage_change(
                baseline['Length Vehicle SUM Empty Ride Hail [km]'],
                fleet_2x['Length Vehicle SUM Empty Ride Hail [km]']
            )
        }
    })
    
    # Analyze 4x fleet impacts
    results['4x_fleet'].update({
        'energy_consumption': {
            'baseline': baseline['Energy VehicleSUM [GJ]'],
            'new': fleet_4x['Energy VehicleSUM [GJ]'],
            'change': calculate_percentage_change(
                baseline['Energy VehicleSUM [GJ]'],
                fleet_4x['Energy VehicleSUM [GJ]']
            )
        },
        'average_speed': {
            'baseline': baseline['Speed VehicleSUM [km/h]'],
            'new': fleet_4x['Speed VehicleSUM [km/h]'],
            'change': calculate_percentage_change(
                baseline['Speed VehicleSUM [km/h]'],
                fleet_4x['Speed VehicleSUM [km/h]']
            )
        },
        'total_vmt': {
            'baseline': baseline['Length VehicleSUM [km]'],
            'new': fleet_4x['Length VehicleSUM [km]'],
            'change': calculate_percentage_change(
                baseline['Length VehicleSUM [km]'],
                fleet_4x['Length VehicleSUM [km]']
            )
        },
        'deadheading_vmt': {
            'baseline': baseline['Length Vehicle SUM Empty Ride Hail [km]'],
            'new': fleet_4x['Length Vehicle SUM Empty Ride Hail [km]'],
            'change': calculate_percentage_change(
                baseline['Length Vehicle SUM Empty Ride Hail [km]'],
                fleet_4x['Length Vehicle SUM Empty Ride Hail [km]']
            )
        }
    })
    
    return results

def print_results(results):
    """Print analysis results in a readable format"""
    print("\n=== 2x Fleet Size Impacts ===")
    
    # Mode share changes
    print("\nMode Share Changes:")
    print(f"Pooled Ridehail: {results['2x_fleet']['pooled_ridehail_share']['baseline']:.2f}% → "
          f"{results['2x_fleet']['pooled_ridehail_share']['new']:.2f}% "
          f"(Change: {results['2x_fleet']['pooled_ridehail_share']['change']:.1f}%)")
    print(f"Solo Ridehail: {results['2x_fleet']['solo_ridehail_share']['baseline']:.2f}% → "
          f"{results['2x_fleet']['solo_ridehail_share']['new']:.2f}% "
          f"(Change: {results['2x_fleet']['solo_ridehail_share']['change']:.1f}%)")
    
    # Wait times
    print("\nWait Time Changes:")
    print(f"Pooled Wait Time: {results['2x_fleet']['pooled_wait_time']['change']:.1f}%")
    print(f"Solo Wait Time: {results['2x_fleet']['solo_wait_time']['change']:.1f}%")
    
    # Environmental impacts
    print("\nEnvironmental Impacts:")
    print(f"Energy Consumption: {results['2x_fleet']['energy_consumption']['change']:.2f}%")
    print(f"Average Speed: {results['2x_fleet']['average_speed']['change']:.2f}%")
    print(f"Total VMT: {results['2x_fleet']['total_vmt']['change']:.2f}%")
    print(f"Deadheading VMT: {results['2x_fleet']['deadheading_vmt']['change']:.2f}%")
    
    print("\n=== 4x Fleet Size Impacts ===")
    print("\nEnvironmental Impacts:")
    print(f"Energy Consumption: {results['4x_fleet']['energy_consumption']['change']:.2f}%")
    print(f"Average Speed: {results['4x_fleet']['average_speed']['change']:.2f}%")
    print(f"Total VMT: {results['4x_fleet']['total_vmt']['change']:.2f}%")
    print(f"Deadheading VMT: {results['4x_fleet']['deadheading_vmt']['change']:.2f}%")

def main():
    # Read the data
    data = pd.read_csv('STs-30pct_final.csv', index_col=0)
    
    # Analyze impacts
    results = analyze_fleet_impacts(data)
    
    # Print results
    print_results(results)
    
    # Create and save the wait time plot
    fig_wait_time = create_wait_time_plot(data)
    fig_wait_time.savefig('wait_time_plot.pdf', bbox_inches='tight', format='pdf')
    plt.close(fig_wait_time)

if __name__ == "__main__":
    main()
