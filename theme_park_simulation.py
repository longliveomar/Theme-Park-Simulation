## -----------------------------------------------------------------------------
## Code Author          : Omar Alaa Eldeen
## Created On           : Sunday - 4th May 2026
## File Name            : theme_park_simulation.py
## Code Title           : Theme Park Ride Simulation
## Description          : This code simulates a theme park ride system using SimPy.
## -----------------------------------------------------------------------------

import simpy
import random
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import messagebox
from tabulate import tabulate

# Constants
RANDOM_SEED = 42
SIMULATION_TIME = 480  # 8 hours
ARRIVAL_RATE = [5, 10, 15]  # Visitors per minute in each phase
RIDE_CAPACITY = 10
NUM_RIDES = 3
RIDE_DURATION = [random.triangular(4, 6, 5) for _ in range(NUM_RIDES)]  # Triangular distribution

# Data tracking
queue_times = []
ride_usage_count = [0] * NUM_RIDES
arrival_times = []
ride_failures = [0] * NUM_RIDES

# Theme Park Environment
class ThemePark:
    def __init__(self, env):
        self.env = env
        self.rides = [simpy.Resource(env, capacity=RIDE_CAPACITY) for _ in range(NUM_RIDES)]
        self.ride_status = [True] * NUM_RIDES  # True = operational

    def ride(self, visitor_id, ride_id):
        yield self.env.timeout(RIDE_DURATION[ride_id])
        print(f"[{self.env.now:>3}m] 🎢 Visitor {visitor_id} finished Ride {ride_id}")

# Visitor Process
def visitor(env, visitor_id, park):
    arrival_time = env.now
    arrival_times.append(arrival_time)
    print(f"[{arrival_time:>3}m] 👤 Visitor {visitor_id} arrived")

    attempts = 0
    ride_id = random.randint(0, NUM_RIDES - 1)
    while not park.ride_status[ride_id] and attempts < 5:
        print(f"[{env.now:>3}m] ❌ Visitor {visitor_id} found Ride {ride_id} out of service.")
        ride_id = random.randint(0, NUM_RIDES - 1)
        attempts += 1

    if not park.ride_status[ride_id]:
        print(f"[{env.now:>3}m] ❌ Visitor {visitor_id} couldn't find any working ride.")
        return

    with park.rides[ride_id].request() as request:
        queue_start = env.now
        yield request
        queue_time = env.now - queue_start
        queue_times.append(queue_time)
        ride_usage_count[ride_id] += 1

        print(f"[{env.now:>3}m] ⏳ Visitor {visitor_id} started Ride {ride_id} after waiting {queue_time:.2f} min")
        yield env.process(park.ride(visitor_id, ride_id))

# Arrival Generator
def arrival_process(env, park):
    visitor_id = 0
    while True:
        current_hour = env.now // 60
        if current_hour < 2:
            rate = ARRIVAL_RATE[0]
        elif current_hour < 4:
            rate = ARRIVAL_RATE[1]
        else:
            rate = ARRIVAL_RATE[2]
        interval = random.expovariate(rate / 60)  # Exponential distribution for interarrival
        yield env.timeout(interval)

        visitor_id += 1
        env.process(visitor(env, visitor_id, park))

# Ride Failure Generator
def ride_failure(env, park, ride_id):
    while True:
        fail_time = random.expovariate(1 / 90)  # ~90 mins between failures
        yield env.timeout(fail_time)
        park.ride_status[ride_id] = False
        ride_failures[ride_id] += 1
        print(f"[{env.now:>3}m] ⚠️ Ride {ride_id} FAILED!")

        repair_time = random.expovariate(1 / 15)  # ~15 mins to repair
        yield env.timeout(repair_time)
        park.ride_status[ride_id] = True
        print(f"[{env.now:>3}m] ✅ Ride {ride_id} REPAIRED.")

# Summary
def print_summary():
    total = len(queue_times)
    avg_q = np.mean(queue_times) if queue_times else 0
    utilization = sum(ride_usage_count) * np.mean(RIDE_DURATION) / (SIMULATION_TIME * NUM_RIDES)

    # Table
    table_data = []
    for i in range(NUM_RIDES):
        table_data.append([f"Ride {i}", ride_usage_count[i], ride_failures[i]])

    headers = ["Ride", "Usage Count", "Failures"]

    print("\n📊 Simulation Results Table:")
    print(tabulate(table_data, headers, tablefmt="pretty"))

    print("\n📊 Simulation Summary:")
    print(f"- Total visitors: {total}")
    print(f"- Average queue time: {avg_q:.2f} minutes")
    print(f"- Average ride utilization: {utilization:.2%}")
    for i, count in enumerate(ride_usage_count):
        print(f"- Ride {i} was used {count} times and failed {ride_failures[i]} times")

    summary = f"📊 Simulation Summary:\n- Total visitors: {total}\n- Avg queue time: {avg_q:.2f} min\n- Utilization: {utilization:.2%}"
    for i, count in enumerate(ride_usage_count):
        summary += f"\n- Ride {i}: {count} uses, {ride_failures[i]} failures"
    messagebox.showinfo("Simulation Summary", summary)

# Plotting
def plot_results():
    plt.figure(figsize=(16, 5))

    plt.subplot(1, 3, 1)
    plt.hist(queue_times, bins=20, color='skyblue', edgecolor='black')
    plt.title("Queue Time Distribution")
    plt.xlabel("Queue Time (min)")
    plt.ylabel("Number of Visitors")

    plt.subplot(1, 3, 2)
    labels = [f"Ride {i}" for i in range(NUM_RIDES)]
    plt.pie(ride_usage_count, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Ride Usage Distribution")

    plt.subplot(1, 3, 3)
    bins = list(range(0, SIMULATION_TIME + 10, 10))
    counts, _ = np.histogram(arrival_times, bins=bins)
    plt.plot(bins[:-1], counts, marker='o', color='green')
    plt.title("Visitor Arrivals Over Time")
    plt.xlabel("Time (min)")
    plt.ylabel("Visitors per 10 min")

    plt.tight_layout()
    plt.show()

# Run Simulation
def run_simulation():
    global queue_times, ride_usage_count, arrival_times, ride_failures
    queue_times = []
    ride_usage_count = [0] * NUM_RIDES
    arrival_times = []
    ride_failures = [0] * NUM_RIDES

    print("🎡 Theme Park Ride Simulation Starting...")
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    park = ThemePark(env)
    env.process(arrival_process(env, park))
    for i in range(NUM_RIDES):
        env.process(ride_failure(env, park, i))
    env.run(until=SIMULATION_TIME)

    print_summary()
    plot_results()
    print("🎡 Simulation Complete!")

# GUI Setup
root = tk.Tk()
root.title("🎢 Theme Park Simulation")
root.geometry("420x250")

label = tk.Label(root, text="Theme Park Ride Simulation", font=("Arial", 16))
label.pack(pady=15)

desc = tk.Label(root, text="Press the button to run the full simulation and view results.",
                font=("Arial", 11))
desc.pack(pady=5)

run_button = tk.Button(root, text="Run Simulation", font=("Arial", 13), command=run_simulation)
run_button.pack(pady=20)

root.mainloop()

