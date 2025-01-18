import numpy as np
import matplotlib as plt

# Function to plot power profile with varying velocities
def plot_power_profiles(velocities, inter, sim_data, plot_solar=True, plot_rolling=True, plot_drag=True, plot_gradient=True, plot_capacity=True):
    """
    Visualizes the instantaneous power draw of the vehicle across various power components while accounting for varying velocities. 
    
    It integrates multiple power profiles, including solar power, rolling resistance, drag resistance, gradient resistance, and battery consumption.
    """
    
    fig, ax1 = plt.subplots(figsize=(24, 16))

    # Calculate cumulative distance using the actual velocities array
    cumulative_distance = np.cumsum(velocities * inter) / 1000  # Convert to kilometers
    cumulative_distance = np.insert(cumulative_distance, 0, 0)

    # Plot the power profiles
    if plot_solar:
        ax1.plot(sim_data[:, 0].mean(axis=0), label='Solar Power (W)')
    if plot_rolling:
        ax1.plot(sim_data[:, 1].mean(axis=0), label='Rolling Resistance (W)')
    if plot_drag:
        ax1.plot(sim_data[:, 2].mean(axis=0), label='Drag Resistance (W)')
    if plot_gradient:
        ax1.plot(sim_data[:, 3].mean(axis=0), label='Gradient Resistance (W)')
    if plot_capacity:
        ax1.plot(sim_data[:, 4].mean(axis=0), label='Battery Capacity (W)')

    # Create the primary x-axis (time) and y-axis (power)
    ax1.set_xlabel('Time (Hours)')
    ax1.set_ylabel('Power (Watts)')
    ax1.set_title('Instantaneous Power Draw with Varying Velocities')
    time_ticks = np.arange(0, len(times))
    time_labels = [f'{i / 4}' for i in range(len(times))]
    ax1.set_xticks(time_ticks, time_labels)

    # Create the secondary x-axis (distance)
    ax2 = ax1.twiny()
    ax2.set_xlabel('Distance (km)')
    distance_ticks = np.arange(0, len(cumulative_distance) - 1) # Set distance ticks based on cumulative distance
    distance_labels = [f'{cumulative_distance[i]:.1f}' for i in distance_ticks]
    ax2.set_xticks(distance_ticks, distance_labels)

    # Mark the stage completion distance
    completion_mark = np.argmax(cumulative_distance >= stage_d)
    if completion_mark < len(cumulative_distance):
        ax1.axvline(x=completion_mark, color='grey', linestyle='--', linewidth=2, label='Stage Completion Distance')

    # Velocity Heatmap Overlay
    norm_velocities = (velocities - min(velocities)) / (max(velocities) - min(velocities))  # Normalize velocities to [0, 1]
    cmap = plt.get_cmap('magma')

    # Overlay the heatmap with increased transparency (alpha)
    for i in range(len(norm_velocities)):
        ax1.axvspan(i, i + 1, color=cmap(norm_velocities[i]), alpha=0.3)

    # Add a color bar for the velocity heatmap
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(velocities), vmax=max(velocities)))
    sm.set_array([])  # Only needed for the color bar
    cbar = plt.colorbar(sm, ax=ax1, alpha=0.3, orientation='vertical', pad=0.02)
    cbar.set_label('Velocity (m/s)', fontsize=12)
    
    ax1.set_xlim(ax2.get_xlim())
    ax1.xaxis.set_ticks_position('bottom')
    ax1.xaxis.set_label_position('bottom')
    ax2.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_label_position('bottom')
    ax2.spines['bottom'].set_position(('outward', 40))

    ax1.legend(loc='upper right')
    ax1.grid(True)

    plt.show(block=True)


def plot_capacity_dynamic(overlay_data, overlay_dist):
    """
    Plots battery capacity dynamically using a velocity array. Overlays true capacity data.
    """
    
    fig, ax1 = plt.subplots(figsize=(24, 16))
    
    # Calculate cumulative distance using the actual velocities array
    cumulative_distance = np.cumsum(velocities * inter) / 1000
    cumulative_distance = np.insert(cumulative_distance, 0, 0)

    # Map overlay distances to time indices using interpolation
    overlay_time_indices = np.interp(overlay_dist, cumulative_distance, np.arange(len(cumulative_distance)))
    ax1.plot(capacity_values.mean(axis=0), label='Predicted Capacity (Wh)', color='blue')
    ax1.plot(overlay_time_indices, overlay_data, label='True Capacity (Wh)', color='red', zorder=5)

    # Create primary x-axis (time) and y-axis (capacity)
    ax1.set_xlabel('Time (Hours)')
    ax1.set_ylabel('Remaining Capacity (Watt-Hours)')
    ax1.set_title('Battery Capacity Over Time and Distance')
    time_ticks = np.arange(0, len(times))
    time_labels = [f'{i / 4}' for i in range(len(times))]
    ax1.set_xticks(time_ticks, time_labels)

    # Create the secondary x-axis (distance)
    ax2 = ax1.twiny()
    ax2.set_xlabel('Distance (km)')
    distance_ticks = np.arange(0, len(cumulative_distance) - 1) # Set distance ticks based on cumulative distance
    distance_labels = [f'{cumulative_distance[i]:.1f}' for i in distance_ticks]
    ax2.set_xticks(distance_ticks, distance_labels)

    # Mark the stage completion distance
    completion_mark = np.argmax(cumulative_distance >= stage_d)
    if completion_mark < len(cumulative_distance):
        ax1.axvline(x=completion_mark, color='grey', linestyle='--', linewidth=2, label='Stage Completion Distance')

    # Velocity Heatmap Overlay
    norm_velocities = (velocities - min(velocities)) / (max(velocities) - min(velocities))  # Normalize velocities to [0, 1]
    cmap = plt.get_cmap('magma')

    # Overlay the heatmap with increased transparency (alpha)
    for i in range(len(norm_velocities)):
        ax1.axvspan(i, i + 1, color=cmap(norm_velocities[i]), alpha=0.3)

    # Add a color bar for the velocity heatmap
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=min(velocities), vmax=max(velocities)))
    sm.set_array([])  # Only needed for the color bar
    cbar = plt.colorbar(sm, ax=ax1, alpha=0.3, orientation='vertical', pad=0.02)
    cbar.set_label('Velocity (m/s)', fontsize=12)

    ax1.set_xlim(ax2.get_xlim())
    ax1.xaxis.set_ticks_position('bottom')
    ax1.xaxis.set_label_position('bottom')
    ax2.xaxis.set_ticks_position('bottom')
    ax2.xaxis.set_label_position('bottom')
    ax2.spines['bottom'].set_position(('outward', 40))

    ax1.legend(loc='upper right')
    ax1.grid(True)

    plt.show()

# User Input
overlay_data = np.array([4000, 4962, 4000, 3700, 200, 2000, 4000])  # real capacity data (Wh)
overlay_dist = np.array([110, 120, 150, 170, 220, 223, 236.80])  # corresponding distance (km)

plot_power_profiles(plot_solar=True, plot_rolling=True, plot_drag=True, plot_gradient=True, plot_consumed=True) # Toggle plots
plot_capacity_dynamic(overlay_data, overlay_dist)