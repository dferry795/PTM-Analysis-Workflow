from os import listdir
from os.path import isfile, join
import sys


def find_score(file: str, position: int) -> float:
    s = 0.0
    with open(f"{mypath}{file}", "r", encoding="utf-8") as scores:
        fir = True
        for row in scores:
            if fir:
                fir = False
                continue
            row_items = row.split()
            pos = int(row_items[0])
            if pos == position:
                s = float(row_items[9])
    return s


def print_set(items: set):
    for item in items:
        if item == "":
            continue
        print("  " + item)


if len(sys.argv) == 9:
    i = sys.argv.index("-m")
    mutationFile = sys.argv[i + 1]
    i = sys.argv.index("-o")
    outFile = sys.argv[i + 1]
    i = sys.argv.index("-p")
    mypath = sys.argv[i+1]
    i = sys.argv.index("-v")
    verifiedFile = sys.argv[i+1]
elif len(sys.argv) >= 3:
    i = sys.argv.index("-m")
    mutationFile = sys.argv[i+1]
    if "-o" in sys.argv:
        i = sys.argv.index("-o")
        outFile = sys.argv[i+1]
    else:
        outFile = "./MutFreq_in_IDR_api.csv"
    if "-p" in sys.argv:
        i = sys.argv.index("-p")
        mypath = sys.argv[i + 1]
    else:
        mypath = "./data/protein_scores/"
    if "-v" in sys.argv:
        i = sys.argv.index("-v")
        verifiedFile = sys.argv[i + 1]
    else:
        verifiedFile = "./data/DisProt_release_2024_12.tsv"
else:
    print("Required arguments:\n\t-m path/mutation_frequency.file\n\nOptional arguments:\n\t-o path/output.file\n\t-p "
          "path/predicted_scores/folder/\n\t-v path/verified_scores.file\n")
    sys.exit(1)

proteinFiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
notFound = {""}

disprot = {}
with open(verifiedFile, "r") as data:
    for line in data:
        if line.startswith("acc"):
            continue
        col = line.split("\t")
        if col[0] not in disprot:
            disprot[col[0]] = [(int(col[7]), int(col[8]))]
        else:
            disprot[col[0]].append((int(col[7]), int(col[8])))

with open(mutationFile, "r", encoding="utf-8") as data, open(outFile, "w", encoding="utf-8") as out:
    first = True
    for line in data:
        lin = line.strip("\n")
        if first:
            first = False
            out.write(lin)
            continue
        col = lin.split(",")
        f = f"{col[0]}.dat"
        if col[0] in disprot:
            for p in disprot[col[0]]:
                if p[0] <= int(col[1]) <= p[1]:
                    out.write(f"\n{lin}")
                    break
        elif f in proteinFiles:
            if find_score(f, int(col[1])) >= 0.5:
                out.write(f"\n{lin}")
        else:
            notFound.add(col[0])

print("Unable to find:")
print_set(notFound)
