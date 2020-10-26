from datetime import datetime

periods = []

print("Stopwatcher v 0.1\n")

def cycle():
    print(f"Periods count: {len(periods)}")
    user_input = input("Press enter to start or any to exit. ")
    if user_input != '':
        return False
    period_start = datetime.now()
    print(f"Timer started at {period_start}.\n")

    user_input = input("Press enter to pause. ")
    period_end = datetime.now()
    periods.append((period_start,period_end))
    print(f"Paused at {period_end}.\n")
    return True

running = True

while running:
    running = cycle()

for i, period in enumerate(periods):
    print(f"{i}\tstart: {period[0]}\tend: {period[1]}")
