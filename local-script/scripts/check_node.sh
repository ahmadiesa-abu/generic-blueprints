VM_IP=$(printf "%d.%d.%d.%d\n" "$((RANDOM % 256))" "$((RANDOM % 256))" "$((RANDOM % 256))" "$((RANDOM % 256))")
ctx logger info "$VM_IP"
ctx instance runtime-properties capabilities "@{}"
ctx instance runtime-properties capabilities.vm_public_ip "$VM_IP"