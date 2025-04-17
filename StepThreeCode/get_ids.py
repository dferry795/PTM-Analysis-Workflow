import sys

if len(sys.argv) >= 3:
    if "-m" in sys.argv:
        i = sys.argv.index("-m")
        file = sys.argv[i+1]
    else:
        print("Required arguments:\n\t-m path/mutation_frequency.file\n\nOptional arguments:\n\t-o path/output.file\n")
        sys.exit(1)
    if "-o" in sys.argv:
        i = sys.argv.index("-o")
        output = sys.argv[i+1]
    else:
        output = "./uniprot_ids.txt"
else:
    print("Required arguments:\n\t-m path/mutation_frequency.file\n\nOptional arguments:\n\t-o path/output.file\n")
    sys.exit(1)

found = {""}
with open(file, "r", encoding="utf-8") as data, open(output, "w", encoding="utf-8") as out:
    spot = 0
    for line in data:
        if spot == 0:
            spot += 1
            continue
        name = line.split("\t")[1]
        if spot == 1:
            spot += 1
            out.write(name)
            found.add(name)
        elif name not in found:
            out.write(f"\n{name}")
            found.add(name)
