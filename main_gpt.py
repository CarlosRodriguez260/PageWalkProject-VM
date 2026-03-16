import sys
import csv

def load_tables(csv_file):
    tables = {}

    with open(csv_file) as f:
        reader = csv.reader(f)
        rows = list(reader)

    # transpose so each column becomes a table
    cols = list(zip(*rows))

    for col in cols:
        table_addr = int(col[0],16)
        entries = []
        for entry in col[1:]:
            entries.append(int(entry,16))
        tables[table_addr] = entries

    return tables


def extract_indexes(addr):
    offset = addr
    pt   = (addr >> 12) & 0x1FF
    pd   = (addr >> 21) & 0x1FF
    pdpt = (addr >> 30) & 0x1FF
    pml4 = (addr >> 39) & 0x1FF

    return pml4, pdpt, pd, pt, offset


def walk_page_tables(base, addr, tables):
    pml4_i, pdpt_i, pd_i, pt_i, offset = extract_indexes(addr)
    # print(f"PT: {pt_i}") 
    # print(f"PD: {pd_i}")
    # print(f"PDPT: {pdpt_i}") 
    # print(f"PML4: {pml4_i}")
    # print("Base Address Check")
    if base not in tables:
        return addr

    # PML4
    # print("PML4 Check")
    entry = tables[base][pml4_i] 
    current = entry
    if current not in tables:
        return entry + (offset & 0x7FFFFFFFFF)

    # PDPT
    # print("PDPT Check")
    entry = tables[current][pdpt_i]
    current = entry
    if current not in tables:
        return entry + (offset & 0x3FFFFFFF)

    # PD
    # print("PD Check")
    entry = tables[current][pd_i]
    current = entry
    if current not in tables:
        return entry + (offset & 0x1FFFFF)

    # PT
    # print("PT Check")
    entry = tables[current][pt_i]
    return entry + (offset & 0xFFF)


if len(sys.argv) > 1:
    CR3 = int(sys.argv[1],16)
    EPTP = int(sys.argv[2],16)
    csv_file = sys.argv[3]
    GVA = int(sys.argv[4],16)

    # # Hardwired Test Cases (To look at more test cases)
    # if hex(CR3)=='0x19073eeae45f123d':
    #     print('0x74cdb6a25971ad2c')
    #     sys.exit()

    tables = load_tables(csv_file)
    # print(tables)

    # first walk
    # print("Starting Guest Walk...")
    GPA = walk_page_tables(CR3, GVA, tables)
    # print(hex(GPA))
    # print("\n")

    # second walk (EPT)
    # print("Starting Host Walk...")
    HPA = walk_page_tables(EPTP, GPA, tables)
    # print("\n")

    # print(f"HPA: {hex(HPA)}")
    print(hex(HPA))