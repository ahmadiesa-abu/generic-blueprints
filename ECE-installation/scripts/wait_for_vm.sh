#!/bin/bash
ctx logger info "Scan for ip"
vm_ip_addr=$(sudo arp-scan -q -l --interface ens192 | grep -i ${MAC_ADDR} | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" | tail -1)
if [ "$vm_ip_addr" == "" ]; then
    ctx retry_operation "VM has no IP yet"
else
    ctx logger info "IP: ${vm_ip_addr}"
    ctx logger info "Check VM SSH"
    ssh_status=$(nc -z "${vm_ip_addr}" 22 > /dev/null && printf "up" || printf "down")
    if [ "$ssh_status" == "down" ]; then
        ctx retry_operation "VM SSH not responding yet"
    else
        ctx instance runtime-properties vm_ip "${vm_ip_addr}"
    fi
fi