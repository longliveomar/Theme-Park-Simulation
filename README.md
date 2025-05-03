# Theme Park Ride Simulation

## Overview
This is a simulation of a theme park with multiple rides, where visitors arrive at different rates depending on the time of day. The simulation tracks the number of visitors, their wait times in queues, and the usage of each ride. The results are displayed in the form of tables, statistics, and plots.

The simulation is built using Python's `SimPy` library for discrete event simulation, `Matplotlib` for plotting, and `Tkinter` for creating a simple graphical user interface (GUI).

## Features
- **Simulated Visitors**: Visitors arrive at the theme park at different rates based on the time of day (e.g., morning, afternoon, and evening).
- **Ride Resources**: The theme park has multiple rides, each with a fixed capacity.
- **Queue System**: Visitors have to wait in a queue before they can board a ride. Queue times are tracked.
- **Ride Usage**: The simulation tracks the number of times each ride is used and calculates the average utilization.
- **Statistics & Plotting**: The simulation provides statistics about visitor flow, average queue times, ride usage, and more. Results are displayed as:
  - A table showing ride usage counts.
  - A bar chart for queue times distribution.
  - A pie chart for ride usage distribution.
  - A line chart showing the number of visitors arriving over time.
- **GUI**: A simple graphical interface that allows users to start the simulation and view the results.

## Requirements
To run this project, you need to install the following Python libraries:
- `SimPy` for simulation (`pip install simpy`)
- `Matplotlib` for plotting (`pip install matplotlib`)
- `Numpy` for data handling (`pip install numpy`)
- `Tabulate` for generating tables (`pip install tabulate`)

Additionally, you can use `Tkinter` for the GUI, which is usually bundled with Python.

## Installation
1. Clone this repository or download the source code.
2. Install the required dependencies:
    ```bash
    pip install simpy matplotlib numpy tabulate
    ```
3. Run the simulation script (`theme_park_simulation.py`).

## Running the Simulation
1. Run the script:
    ```bash
    python theme_park_simulation.py
    ```
2. The GUI window will open. Click the **Run Simulation** button to start the simulation.
3. The simulation will run for 8 hours, tracking the visitor arrivals, queue times, and ride usage.
4. Once the simulation is complete, a summary of results will be displayed in a table format and as charts.

## Output
The simulation produces the following output:
- A **simulation table** showing the usage count of each ride.
- **Statistics** about the total number of visitors, average queue time, and ride utilization.
- **Plots**:
  - Queue time distribution (Histogram).
  - Ride usage distribution (Pie chart).
  - Visitor arrivals over time (Line chart).

Additionally, a **summary message** will be displayed via the GUI, containing:
- Total number of visitors.
- Average queue time.
- Ride usage breakdown.
- Average ride utilization.

## Example Output

### Simulation Results Table:
