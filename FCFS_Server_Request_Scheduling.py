import matplotlib.pyplot as plt
from tabulate import tabulate

# --------------------------
# Step 1: Input Server Requests
# --------------------------
def get_requests_input():
    requests = []
    n = int(input("Enter number of server requests: "))

    for i in range(n):
        req_id = f'Req{i + 1}'
        arrival = int(input(f"Enter arrival time for {req_id}: "))
        process = int(input(f"Enter processing time for {req_id}: "))
        requests.append({
            'id': req_id,
            'arrival_time': arrival,
            'processing_time': process
        })

    return requests

# --------------------------
# Step 2: FCFS Scheduling
# --------------------------
def fcfs_schedule(requests):
    requests.sort(key=lambda r: r['arrival_time'])
    current_time = 0
    idle_time = 0

    for req in requests:
        req['start_time'] = max(current_time, req['arrival_time'])

        # Track idle time
        if current_time < req['arrival_time']:
            idle_time += req['arrival_time'] - current_time

        req['completion_time'] = req['start_time'] + req['processing_time']
        req['waiting_time'] = req['start_time'] - req['arrival_time']
        req['turnaround_time'] = req['completion_time'] - req['arrival_time']
        req['status'] = 'Completed'
        current_time = req['completion_time']

    return idle_time

# --------------------------
# Step 3: Display Result Table
# --------------------------
def display_request_table(requests):
    table = [
        [r['id'], r['arrival_time'], r['processing_time'], r['start_time'],
         r['completion_time'], r['waiting_time'], r['turnaround_time'], r['status']]
        for r in requests
    ]
    headers = ["Request ID", "Arrival", "Processing", "Start", "Completion",
               "Waiting", "Turnaround", "Status"]
    print("\n Server Request Execution Table:")
    print(tabulate(table, headers, tablefmt="grid"))

# --------------------------
# Step 4: Gantt Chart (Improved)
# --------------------------
def draw_gantt_chart(requests):
    fig, gnt = plt.subplots(figsize=(10, 2))
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Requests")
    gnt.set_yticks([15])
    gnt.set_yticklabels(["Server"])
    gnt.grid(True)

    colors = ['tab:blue', 'tab:green', 'tab:red', 'tab:orange', 'tab:purple']
    
    for i, r in enumerate(requests):
        gnt.broken_barh([(r['start_time'], r['processing_time'])],
                        (10, 9), facecolors=colors[i % len(colors)])
        gnt.text(r['start_time'] + r['processing_time'] / 2 - 0.5,
                 13, r['id'], color='white', weight='bold')

    plt.title("Gantt Chart - FCFS Server Scheduling")
    plt.tight_layout()
    plt.show()

# --------------------------
# Step 5: Metrics Calculation
# --------------------------
def calculate_metrics(requests, idle_time):
    total_requests = len(requests)
    total_time = requests[-1]['completion_time'] if requests else 0
    total_processing = sum(r['processing_time'] for r in requests)

    avg_wt = sum(r['waiting_time'] for r in requests) / total_requests
    avg_tat = sum(r['turnaround_time'] for r in requests) / total_requests
    server_util = ((total_processing) / total_time) * 100 if total_time > 0 else 0

    print("\n Performance Metrics:")
    print(f"Total Time Elapsed           : {total_time}")
    print(f"Total Idle Time              : {idle_time}")
    print(f"Average Waiting Time         : {avg_wt:.2f}")
    print(f"Average Turnaround Time      : {avg_tat:.2f}")
    print(f"Server Utilization (%)       : {server_util:.2f}%")

# --------------------------
# Step 6: Run Full Program
# --------------------------
if __name__ == "__main__":
    print("🔧 Server Request Management System - FCFS Scheduling")
    server_requests = get_requests_input()
    idle_time = fcfs_schedule(server_requests)
    display_request_table(server_requests)
    draw_gantt_chart(server_requests)
    calculate_metrics(server_requests, idle_time)
