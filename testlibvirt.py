import libvirt
import time

def connect_to_hypervisor():
    conn = libvirt.open('qemu:///system')
    return conn

def create_vm(xmlfile, conn):
    with open(xmlfile, 'r') as vm_file:
        vmconfig = vm_file.read()
    vm = conn.createXML(vmconfig, 0)
    if vm:
        print('VM creada')
        conn.close()

def find_vm_by_name(name, conn):
    for domain in conn.listAllDomains():
        if domain.name() == name:
            return domain
        return None

def start_vm(domain):
    if domain:
        domain.create()
        print(domain.name(), " iniciada")
    else:
        print("No existe esa vm")

def shutdown_vm(domain):
    domain.shutdown()
    print(domain.name(), " apagada")


def save_vm(vm, path):
    vm.save(path)
    print(vm.name(), " guardada en: ",path)

def restore_vm(conn, path):
    conn.restore(path)
    print("Máquina virtual restaurada")

def get_cpu_usage(vm, sleeptime):
    initial_cpu_time = vm.getCPUStats(True)[0]['cpu_time']
    time.sleep(sleeptime)
    final_cpu_time = vm.getCPUStats(True)[0]['cpu_time']
    cpu_usage = round((final_cpu_time - initial_cpu_time) / (sleeptime*1000000000) * 100,4)
    return cpu_usage

"CPU Usage (%) = ((Final CPU Time - Initial CPU Time) / Elapsed Time) * 100"


def get_stats_vm(vm, time):
    periods = time/5
    for i in range (0,int(periods)):
        if i > 0:
            cpu_usage = get_cpu_usage(vm, 5)
            print("CPU usage: ", cpu_usage, "%")
        memory_usage = round(vm.memoryStats()['rss']/1024/1024,4)
        print("Memory usage: ", memory_usage, "GB")


def main():
    conn = connect_to_hypervisor()
    #create_vm('vm.xml', conn)
    vm = find_vm_by_name("ubuntu22.04", conn)
    #start_vm(vm)
    #save_vm(vm, 'lastvmstate.sav')
    #restore_vm(conn, 'lastvmstate.sav')
    #shutdown_vm(vm)
    get_stats_vm(vm, 60)

main()