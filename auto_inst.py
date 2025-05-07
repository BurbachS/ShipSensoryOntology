import pandas as pd
from collections import defaultdict


# --- CONFIGURATION ---
ONTOLOGY_IN    = "Ontology/ship_ontology.ttl"
ONTOLOGY_OUT   = "Ontology/instantiated_ship_ontology.ttl"
EXCEL_FILE     = "Property_Matrix/OWL_Property_Matrix.xlsx"

EX_PREFIX_LINE = "@prefix ex: <http://example.org/individuals#> .\n"

INSTANCES_MARKER = """
#################################################################

# Ontology Instances

#################################################################

"""

# Read existing ontology ---
with open(ONTOLOGY_IN, 'r', encoding='utf-8') as f:
    ontology_body = f.read()

# Read each sheet one by one and build a small TTL block 
sheets = pd.read_excel(EXCEL_FILE, sheet_name=None)
final_ttl = ""
for sheet_name, df in sheets.items():
    # Skip empty sheets if you like
    if df.empty:
        continue

    # final_ttl += f"
    # Instances from sheet: {sheet_name} \n"
    cols = df.columns.tolist()
    if "Individual" not in cols:
        raise KeyError(f"Sheet {sheet_name!r} has no 'Individual' column")

    predicates = cols[1:]  # everything else after 'Individual'

    # Generate TTL for each row in this sheet
    for _, row in df.iterrows():
        subj = str(row["Individual"]).strip()
        if not subj or pd.isna(subj):
            continue

        # Collect prop list of objects
        pmap = defaultdict(list)
        for prop in predicates:
            cell = row[prop]
            if pd.notna(cell) and str(cell).strip():
                for raw in str(cell).split(','):
                    v = raw.strip()
                    if not v:
                        continue
                    if prop == "rdf:type":
                        pmap["a"].append(v)
                    else:
                        pmap[prop].append(f"ex:{v}")

        # Format the triples block
        final_ttl += f"ex:{subj} "
        triples = []
        for p, objs in pmap.items():
            objs_s = " , ".join(objs)
            triples.append(f"{p} {objs_s}")

        final_ttl += " ;\n    ".join(triples) + " .\n\n"

# Compose full output
with open(ONTOLOGY_OUT, 'w', encoding='utf-8') as f:
    # 2) ex: prefix first
    f.write(EX_PREFIX_LINE)
    # original ontology
    f.write(ontology_body.rstrip() + "\n")
    # 3) marker
    f.write(INSTANCES_MARKER)
    # 4) appended instances
    f.write(final_ttl)

print(f"✅ Written merged ontology + individuals to `{ONTOLOGY_OUT}`")
