import psutil
import platform

cpu_freq = psutil.cpu_freq()
cpu_perc = psutil.cpu_percent()
main_mem = psutil.virtual_memory()

# Verhindert dass Monitoring beim Import ausgeführt wird
if __name__ == "__main__":
    print("="*5, "CPU Info", "="*5)

    # CPU Frequenzen
    print(cpu_freq)
    print("Current Frequency: ", cpu_freq.current)

    # CPU Nutzung
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")


    print("="*5, "Memory Information", "="*5)

    # Speicherdetails
    print("Available: ", main_mem.available)
    print("Used: ", main_mem.used)
    print("Percentage: ", main_mem.percent)
