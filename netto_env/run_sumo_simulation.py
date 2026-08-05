import os
import csv
import subprocess
import traci
import sumolib

# Define the file paths
sumo_cfg_file = "ABS.sumocfg"
net_file = "expjac.net.xml"
route_file = "ABS_intersection.rou.xml"
output_file = os.path.join(os.getcwd(), "output_simulation.csv")  # Use current directory

# Function to run the SUMO simulation and collect data
def run_sumo_simulation():
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir:  # Only create directory if it's not empty
        os.makedirs(output_dir, exist_ok=True)

    # Check if input files exist
    for file in [sumo_cfg_file, net_file, route_file]:
        if not os.path.exists(file):
            print(f"Error: File {file} not found.")
            return

    # Start the SUMO simulation with TraCI and GUI
    sumo_command = [
        "sumo-gui",  # Use GUI for visualization
        "-c", sumo_cfg_file,
        "--net-file", net_file,
        "--route-files", route_file,
        "--output-prefix", "output_simulation",
        "--collision.check-junctions", "true"  # Enable collision detection at junctions
    ]

    try:
        # Start TraCI
        print("Starting TraCI with SUMO-GUI...")
        traci.start(sumo_command, numRetries=10)
        print("TraCI started successfully.")

        # Check initial simulation state
        min_expected = traci.simulation.getMinExpectedNumber()
        print(f"Initial minExpectedNumber: {min_expected}")
        if min_expected == 0:
            print("Warning: No vehicles expected in the simulation. Check ABS_intersection.rou.xml for valid vehicle definitions and routes.")

        # Open CSV file to write results
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['step', 'system_total_stopped', 'agents_total_stopped', 
                            'system_total_waiting_time', 'system_mean_waiting_time', 
                            'system_mean_speed', 'collisions'])

            step = 0
            max_steps = 1900  # Match sumocfg end time
            while traci.simulation.getMinExpectedNumber() > 0 and step < max_steps:
                traci.simulationStep()  # Advance the simulation by one step

                # Get all vehicle IDs
                vehicle_ids = traci.vehicle.getIDList()
                print(f"Step {step}: Number of vehicles = {len(vehicle_ids)}")  # Debug

                # Initialize metrics
                total_stopped = 0
                agents_stopped = 0  # Assuming same logic as system_total_stopped
                total_waiting_time = 0
                total_speed = 0
                vehicle_count = len(vehicle_ids)
                collisions = len(traci.simulation.getCollisions())  # Count collisions

                # Collect data for each vehicle
                for veh_id in vehicle_ids:
                    speed = traci.vehicle.getSpeed(veh_id)
                    waiting_time = traci.vehicle.getWaitingTime(veh_id)
                    # Consider a vehicle stopped if its speed is very low (< 0.1 m/s)
                    if speed < 0.1:
                        total_stopped += 1
                        agents_stopped += 1  # Same logic unless specified otherwise
                    total_waiting_time += waiting_time
                    total_speed += speed

                # Calculate mean values
                mean_waiting_time = total_waiting_time / vehicle_count if vehicle_count > 0 else 0
                mean_speed = total_speed / vehicle_count if vehicle_count > 0 else 0

                # Write to CSV
                writer.writerow([step, total_stopped, agents_stopped, total_waiting_time, 
                                mean_waiting_time, mean_speed, collisions])
                print(f"Step {step}: Stopped={total_stopped}, AgentsStopped={agents_stopped}, "
                      f"WaitingTime={total_waiting_time}, MeanWaitingTime={mean_waiting_time}, "
                      f"MeanSpeed={mean_speed}, Collisions={collisions}")  # Debug

                step += 1

            if step == 0:
                print("Warning: Simulation ended immediately. No vehicles detected. "
                      "Check ABS_intersection.rou.xml for valid vehicle definitions and routes. "
                      "Ensure routes use valid edge IDs from expjac.net.xml.")

        # Close TraCI connection
        traci.close()
        print("Simulation complete and data saved to CSV.")

    except subprocess.CalledProcessError as e:
        print(f"SUMO error: {e}")
    except traci.TraCIException as e:
        print(f"TraCI error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        # Ensure TraCI closes even if an error occurs
        if traci.isLoaded():
            traci.close()

# Run the simulation
run_sumo_simulation()