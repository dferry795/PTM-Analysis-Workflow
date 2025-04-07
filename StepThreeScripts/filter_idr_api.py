import sys
import requests
import json

if len(sys.argv) == 7:
    i = sys.argv.index("-m")
    mutationFile = sys.argv[i + 1]
    i = sys.argv.index("-o")
    outFile = sys.argv[i + 1]
    i = sys.argv.index("-v")
    verifiedFile = sys.argv[i+1]
elif len(sys.argv) >= 3:
    if "-m" in sys.argv:
        i = sys.argv.index("-m")
        mutationFile = sys.argv[i+1]
    else:
        print("Required arguments:\n\t-m path/mutation_frequency.file\n\nOptional arguments:\n\t-o path/output.file\n\t"
              "-v path/verified_scores.file\n")
        sys.exit(1)
    if "-o" in sys.argv:
        i = sys.argv.index("-o")
        outFile = sys.argv[i+1]
    else:
        outFile = "./MutFreq_in_IDR_api.csv"
    if "-v" in sys.argv:
        i = sys.argv.index("-v")
        verifiedFile = sys.argv[i + 1]
    else:
        verifiedFile = ""
else:
    print("Required arguments:\n\t-m path/mutation_frequency.file\n\nOptional arguments:\n\t-o path/output.file\n\t"
          "-v path/verified_scores.file\n")
    sys.exit(1)

url = "https://aiupred.elte.hu/rest_api"

disprot = {}
if verifiedFile != "":
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
    found = {}
    for line in data:
        lin = line.strip("\n")
        if first:
            first = False
            out.write(lin)
            continue
        col = lin.split(",")
        f = f"{col[2]}.dat"
        if col[2] in disprot:
            for p in disprot[col[2]]:
                if p[0] <= int(col[3]) <= p[1]:
                    out.write(f"\n{lin}")
                    break
        elif col[2] in found:
            for p in found[col[2]]:
                if p[0] <= int(col[3]) <= p[1]:
                    out.write(f"\n{lin}")
        else:
            par = {"accession": col[2], "smoothing": "default", "analysis_type": "redox"}
            results = json.loads(requests.get(url, params=par).text)
            found[col[2]] = results["regions"]
            for bounds in results["regions"]:
                if bounds[0] <= int(col[3]) <= bounds[1]:
                    out.write(f"\n{lin}")
                    break
