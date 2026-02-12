from flask import Flask, request, jsonify
import uuid
import time
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

# In-memory storage for mock data
hypothesis_requests = {}

@app.route('/api/mock/hypothesis/projects', methods=['GET'])
def list_or_get_project():
    """
    List all available user projects OR get details for a specific project
    """
    project_id = request.args.get("id")
    logger.info(f"---> GET /projects?id={project_id}")

    # Hardcoded project data
    projects_db = {
        "project_abc123": {
            "id": "project_abc123",
            "name": "Obesity Study",
            "hypotheses": [{"variant": "rs1421985"}, {"variant": "rs9939609"}],
            "ldsc": {
                "tissues": [{"name": "Adipose_Subcutaneous"}, {"name": "Brain_Cortex"}]
            }
        },
        "project_xyz789": {
            "id": "project_xyz789",
            "name": "Diabetes Study",
            "hypotheses": [{"variant": "rs7903146"}],
            "ldsc": {
                "tissues": [{"name": "Pancreas"}, {"name": "Liver"}]
            }
        }
    }

    if project_id:
        if project_id not in projects_db:
            return jsonify({"error": "Project not found"}), 404
        return jsonify(projects_db[project_id])
    
    # If no ID, return list
    return jsonify({
        "projects": [
            {"id": "project_abc123", "name": "Obesity Study"},
            {"id": "project_xyz789", "name": "Diabetes Study"}
        ]
    })

@app.route('/api/mock/hypothesis/enrich', methods=['POST'])
def start_enrich():
    """Step 1: Start enrichment"""
    logger.info(f"---> POST /enrich | Payload: {request.json}")
    req_id = f"hyp_{uuid.uuid4().hex[:8]}"
    variant = request.json.get("variant", "rs1421985")  #rs1421085
    hypothesis_requests[req_id] = {
        "status": "pending",
        "created_at": datetime.datetime.now(datetime.UTC),
        "enrich_id": f"enrich_{uuid.uuid4().hex[:8]}",
        "variant": variant
    }
    return jsonify({
        "hypothesis_id": req_id,
        "project_id": request.json.get("project_id")
    }), 202

@app.route('/api/mock/hypothesis/hypothesis', methods=['GET'])
def check_status():
    """Step 2: Check status (Polling)"""
    req_id = request.args.get("id")
    if not req_id or req_id not in hypothesis_requests:
        return jsonify({"error": "Hypothesis ID not found"}), 404
    
    data = hypothesis_requests[req_id]
    
    # Simulate processing time (e.g., 5 seconds)
    time_diff = (datetime.datetime.now(datetime.UTC) - data["created_at"]).total_seconds()
    if time_diff > 5:
        data["status"] = "completed"
    
    logger.info(f"---> GET /hypothesis?id={req_id} | Status: {data['status']}")
    
    return jsonify({
        "id": req_id,
        "status": data["status"],
        "phenotype": "Obesity",
        "enrich_id": data["enrich_id"]
    })

@app.route('/api/mock/hypothesis/enrich', methods=['GET'])
def get_enrich():
    """Step 3: Get enrichment results"""
    enrich_id = request.args.get("id")
    logger.info(f"---> GET /enrich?id={enrich_id}")
    return jsonify({
        "id": request.args.get("id"),
        "causal_gene": "FTO",
        "GO_terms": [
            {"id": "GO:1904177", "name": "Regulation of Adipose Tissue Development"}
        ]
    })

@app.route('/api/mock/hypothesis/hypothesis', methods=['POST'])
def final_hypothesis():
    """Step 4: Generate final hypothesis"""
    logger.info(f"---> POST /hypothesis (Generate) | Payload: {request.json}")
    enrich_id = request.json.get("id")
    
    # Find the variant used for this enrichment
    variant = "rs1421985" # Default fallback
    for req in hypothesis_requests.values():
        if req.get("enrich_id") == enrich_id:
            variant = req.get("variant")
            break

    return jsonify({
        "summary": f"Mocked hypothesis summary for variant {variant}",
        "graph": {
            "nodes": [
                {"id": variant, "type": "snp", "name": variant},
                {"id": "FTO", "type": "gene", "name": "FTO"},
                {"id": "GO:1904177", "type": "go", "name": "Regulation of Adipose Tissue Development"}
            ],
            "edges": [
                {"source": variant, "target": "FTO", "label": "affects"},
                {"source": "FTO", "target": "GO:1904177", "label": "involved_in"}
            ],
            "probability": 0.95
        }
    }), 201

if __name__ == "__main__":
    print("Starting Mock Hypothesis Server on port 9001...")
    app.run(host='0.0.0.0', port=9001, debug=True)
