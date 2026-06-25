import json
from pathlib import Path
from flask import Flask, render_template, jsonify

app = Flask(__name__)

def load_graph_content():
    path = Path("data/profiles/graph_content.json")
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)

def load_cluster_labels():
    path = Path("data/profiles/cluster_labels.json")
    if not path.exists():
        return None
    with open(path) as f:
        return json.load(f)

@app.route("/")
def index():
    return render_template("graph.html")

@app.route("/api/profile")
def profile():
    content = load_graph_content()
    clusters = load_cluster_labels()

    if not content:
        return jsonify({"error": "no profile found"}), 404

    # build nodes and edges dynamically
    nodes = []
    edges = []
    node_id = 0
    label_to_id = {}

    # palette node — anchor
    nodes.append({
        "id": node_id,
        "label": content["palette"]["name"],
        "type": "palette",
        "desc": f"{', '.join(content['palette']['hex_codes'])}\n\n{content['palette']['mood']}"
    })
    label_to_id[content["palette"]["name"]] = node_id
    node_id += 1

    # archetype nodes
    for arch in content["archetypes"]:
        nodes.append({
            "id": node_id,
            "label": arch["label"],
            "type": "archetype",
            "desc": arch["desc"]
        })
        label_to_id[arch["label"]] = node_id

        # connect to palette
        edges.append([label_to_id[content["palette"]["name"]], node_id])

        # motif nodes
        for motif in arch["motifs"][:3]:
            if motif not in label_to_id:
                nodes.append({
                    "id": node_id + 1,
                    "label": motif,
                    "type": "motif",
                    "desc": f"A recurring visual motif in your {arch['label']} cluster."
                })
                label_to_id[motif] = node_id + 1
                node_id += 1
            edges.append([label_to_id[arch["label"]], label_to_id[motif]])

        node_id += 1

    # brand nodes
    for brand in content["brands"]:
        nodes.append({
            "id": node_id,
            "label": brand["label"],
            "type": "brand",
            "desc": brand["desc"],
            "url": brand.get("url", ""),
            "category": brand.get("category", "")
        })
        label_to_id[brand["label"]] = node_id

        # connect brand to matching archetype
        for arch in content["archetypes"]:
            if any(word in arch["label"] for word in brand["label"].lower().split()):
                edges.append([label_to_id[arch["label"]], node_id])
                break
        else:
            # connect to first archetype as fallback
            edges.append([nodes[1]["id"], node_id])

        node_id += 1

    # read nodes
    for read in content["reads"]:
        nodes.append({
            "id": node_id,
            "label": read["label"][:30] + "..." if len(read["label"]) > 30 else read["label"],
            "type": "reading",
            "desc": read["desc"],
            "url": read.get("url", ""),
            "publication": read.get("publication", "")
        })
        label_to_id[read["label"]] = node_id

        # connect to scholarly chic or first archetype
        connected = False
        for arch in content["archetypes"]:
            if "scholarly" in arch["label"] or "urban" in arch["label"]:
                edges.append([label_to_id[arch["label"]], node_id])
                connected = True
                break
        if not connected:
            edges.append([nodes[1]["id"], node_id])

        node_id += 1

    # feature
    feature = content.get("feature", "")

    return jsonify({
        "nodes": nodes,
        "edges": edges,
        "feature": feature,
        "palette": content["palette"]
    })

if __name__ == "__main__":
    app.run(debug=True)