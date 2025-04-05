import sys

if len(sys.argv) >= 5:
    if "-p" in sys.argv:
        phaseFiles = []
        i = sys.argv.index("-p")
        for num in range(i+1, len(sys.argv)):
            if sys.argv[num] == "-d" or sys.argv[num] == "-o":
                break
            phaseFiles.append(sys.argv[num])
    else:
        print("Required arguments:\n\t-p path/phase_separation.file\n\t-d path/MutFreq_in_IDR.file\n\nOptional "
              "arguments:\n\t-o path/output.file\n\t")
        sys.exit(1)
    if "-d" in sys.argv:
        i = sys.argv.index("-d")
        disorderFile = sys.argv[i+1]
    else:
        print("Required arguments:\n\t-p path/phase_separation.file\n\t-d path/MutFreq_in_IDR.file\n\nOptional "
              "arguments:\n\t-o path/output.file\n\t")
        sys.exit(1)
    if "-o" in sys.argv:
        i = sys.argv.index("-o")
        output = sys.argv[i+1]
    else:
        output = "./MutFreq_in_IDR_and_PS.csv"
else:
    print("Required arguments:\n\t-p path/phase_separation.file\n\t-d path/MutFreq_in_IDR.file\n\nOptional arguments:"
          "\n\t-o path/output.file\n\t")
    sys.exit(1)

names = {}
for file in phaseFiles:
    with open(file, "r", encoding="utf-8") as data:
        for line in data:
            if line.startswith(">"):
                col = line.strip("\n").split()
                name = col[2][:-1]
                if name in names:
                    names[name].append(col[4].split("-"))
                else:
                    names[name] = [col[4].split("-")]

with open(disorderFile, "r", encoding="utf-8") as data, open(output, "w", encoding="utf-8") as out:
    first = True
    for line in data:
        lin = line.strip("\n")
        if first:
            out.write(lin)
            first = False
            continue
        col = line.split(",")
        if col[0] in names:
            for bounds in names[col[0]]:
                if int(bounds[0]) <= int(col[1]) <= int(bounds[1]):
                    out.write(f"\n{lin}")
                    break
