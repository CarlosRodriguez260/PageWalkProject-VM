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
        table_addr = col[0]
        entries = list(col[1:])
        tables[table_addr] = entries

    return tables

if len(sys.argv) > 1:
    # print("\nStarting Page Walk...")
    tables = load_tables(sys.argv[3])
    # print(tables)
    # print("\n")

    # Parse Arguments
    CR3 = int(sys.argv[1], 16)
    EPT_PTR = int(sys.argv[2], 16)
    GVA = int(sys.argv[4], 16)

    # Turn GVA into indexes
    offset = GVA & 0xFFF
    pt_i    = (GVA >> 12) & 0x1FF
    pd_i     = (GVA >> 21) & 0x1FF
    pdpt_i   = (GVA >> 30) & 0x1FF
    pml4_i   = (GVA >> 39) & 0x1FF
    print(f"Offset: {offset}") # Fine
    print(f"PT: {pt_i}") # Fine
    print(f"PD: {pd_i}") # Fine
    print(f"PDPT: {pdpt_i}") 
    print(f"PML4: {pml4_i}\n")

    # Guest Page Walk
    current_table = hex(CR3)
    print(current_table)
    print(f"{pml4_i} | {pml4_i+2} in excel.\n")
    pml4_entry = tables[current_table][pml4_i] # Use modulus if entries < 512
    current_table = pml4_entry

    print(current_table)
    print(f"{pdpt_i} | {pdpt_i+2} in excel.\n")
    pdpt_entry = tables[current_table][pdpt_i]
    current_table = pdpt_entry

    print(current_table)
    print(f"{pd_i} | {pd_i+2} in excel.\n")
    pd_entry = tables[current_table][pd_i]
    current_table = pd_entry

    pt_entry = tables[current_table][pt_i]
    GPA = int(pt_entry, 16) + offset 
    # print(f"Final GPA: {hex(GPA)}")
    print(hex(GPA))

    # Turn GPA into indexes
    # offset = GPA & 0xFFF
    # pt_i    = (GPA >> 12) & 0x1FF
    # pd_i     = (GPA >> 21) & 0x1FF
    # pdpt_i   = (GPA >> 30) & 0x1FF
    # pml4_i   = (GPA >> 39) & 0x1FF

    # # Host Page Walk
    # current_table = hex(EPT_PTR)
    # pml4_entry = tables[current_table][pml4_i] # Use modulus if entries < 512
    # current_table = pml4_entry

    # pdpt_entry = tables[current_table][pdpt_i]
    # current_table = pdpt_entry

    # pd_entry = tables[current_table][pd_i]
    # current_table = pd_entry

    # pt_entry = tables[current_table][pt_i]
    # HPA = int(pt_entry, 16) + offset 
    # # print(f"Final HPA: {hex(HPA)}")
    # print(HPA)

# GUEST_PML4_base = sys.argv[]

    # # Hex to Binary Mapper
    # hex_bin_map = {
    #     '0':'0000',
    #     '1':'0001',
    #     '2':'0010',
    #     '3':'0011',
    #     '4':'0100',
    #     '5':'0101',
    #     '6':'0110',
    #     '7':'0111',
    #     '8':'1000',
    #     '9':'1001',
    #     'A':'1010',
    #     'B':'1011',
    #     'C':'1100',
    #     'D':'1101',
    #     'E':'1110',
    #     'F':'1111',
    # }

    # # Switch GVA from hex to binary string
    # binary = ''
    # for hex in sys.argv[4][2:].upper():
    #     print(f"Hex: {hex} -> Binary: {hex_bin_map[hex]}")

    #     if len(binary) == 0 and hex=='0':
    #         continue
    #     binary += hex_bin_map[hex]
    # print(binary)

    # if len(binary)!=48:
    #     raise ValueError(f"Total bit count: {len(binary)}. Incorrect! Must be 48.")
    # print(f"Total bit count: {len(binary)}")