import sys
import csv

def load_tables(csv_file):
    tables = {}

    with open(csv_file) as f:
        reader = csv.reader(f)
        rows = list(reader)

    cols = list(zip(*rows))

    for col in cols:
        table_addr = int(col[0],16)
        entries = []
        for entry in col[1:]:
            entries.append(int(entry,16))
        tables[table_addr] = entries

    return tables


def extract_indexes(addr):
    offset = addr & 0xFFF
    pt   = (addr >> 12) & 0x1FF
    pd   = (addr >> 21) & 0x1FF
    pdpt = (addr >> 30) & 0x1FF
    pml4 = (addr >> 39) & 0x1FF

    return pml4, pdpt, pd, pt, offset

def x_walk(base, addr, tables):
    pml4_i, pdpt_i, pd_i, pt_i, offset = extract_indexes(addr)
    # print("X-Walk...")
    # print(f"PT: {pt_i}") 
    # print(f"PD: {pd_i}")
    # print(f"PDPT: {pdpt_i}") 
    # print(f"PML4: {pml4_i}")
    # print(f"Offset: {offset}")
    # print("Base Address Check")
    if base not in tables:
        return addr

    # PML4
    # print("PML4 Check")
    entry = tables[base][pml4_i] 
    current = entry
    # print(hex(current))
    if current not in tables:
        # print("X-Walk done...")
        return entry + offset
    

    # PDPT
    # print("PDPT Check")
    entry = tables[current][pdpt_i]
    current = entry
    # print(hex(current))
    if current not in tables:
        # print("X-Walk done...")
        return entry + offset

    # PD
    # print("PD Check")
    entry = tables[current][pd_i]
    current = entry
    # print(hex(current))
    if current not in tables:
        # print("X-Walk done...")
        return entry + offset

    # PT
    # print("PT Check")
    entry = tables[current][pt_i]
    # print(hex(entry+offset))
    # print("X-Walk done...")
    return entry + offset

# Main
if len(sys.argv) > 1:
    CR3 = int(sys.argv[1],16) # Guest Page Table
    EPTP = int(sys.argv[2],16) # Host (EPT)
    csv_file = sys.argv[3]
    GVA = int(sys.argv[4],16) 
    tables = load_tables(csv_file)

    pml4_i, pdpt_i, pd_i, pt_i, offset = extract_indexes(GVA)
    # print(f"PT: {pt_i}") 
    # print(f"PD: {pd_i}")
    # print(f"PDPT: {pdpt_i}") 
    # print(f"PML4: {pml4_i}")
    # print(f"Offset: {offset}")
    # print("Base Address Check")
    if CR3 not in tables:
        print(hex(GVA))
        sys.exit()

    # PML4
    # print("PML4 Check")
    # print(hex(CR3))
    entry = tables[CR3][pml4_i] 
    current = entry
    # print(hex(current))
    if current not in tables:
        current = x_walk(EPTP, current, tables)
        current = tables[current][pt_i]
        current += offset
        print(hex(current))
        sys.exit()
    
  
    # PDPT
    # print("PDPT Check")
    entry = tables[current][pdpt_i]
    current = entry
    # print(hex(current))
    if current not in tables:
        current = x_walk(EPTP, current, tables)
        current = tables[current][pt_i]
        current += offset
        print(hex(current))
        sys.exit()
    
    
    # PD
    # print("PD Check")
    entry = tables[current][pd_i]
    current = entry
    if current not in tables:
        current = x_walk(EPTP, current, tables)
        current = tables[current][pt_i]
        current += offset
        print(hex(current))
        sys.exit()
    
    # PT
    # print("PT Check")
    if current in tables:
        entry = tables[current][pt_i]
        print(hex(x_walk(EPTP, entry, tables) + offset))
    else:
        print(hex(current+ offset))