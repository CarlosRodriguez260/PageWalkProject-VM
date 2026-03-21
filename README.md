# PageWalkProject-VM

## Extended Page Tables:
- *Extended page tables* combine in hardware the classic hardware-defined page table structure of the x86, maintained by the guest OS with a second page table structure maintained by the hypervisor which specifies guest-physical to host-physical mappings.
- The *Extended Page Table Pointer (EPTP)* is a table that points into the extended page (host memory).

## Address Path:
Guest Virtual -> Guest Physical -> Host Physical

![alt text](image.png)
![alt text](image-1.png)