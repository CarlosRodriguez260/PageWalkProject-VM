# PageWalkProject-VM

## Extended Page Tables:
- *Extended page tables* combine in hardware the classic hardware-defined page table structure of the x86, maintained by the guest OS with a second page table structure maintained by the hypervisor which specifies guest-physical to host-physical mappings.
- The *Extended Page Table Pointer (EPTP)* is a table that points into the extended page (host memory).

## Address Path:
Guest Virtual -> Guest Physical -> Host Physical

![alt text](image.png)
![alt text](image-1.png)

## Rough Program Flow:
parse args

virtual_address = input

split virtual address into:
    pml4_i
    pdpt_i
    pd_i
    pt_i
    offset

guest_phys = guest_page_walk(CR3)

host_phys = ept_page_walk(EPTP, guest_phys)

print(host_phys)
