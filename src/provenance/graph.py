import uuid
from typing import Optional

class ProvenanceNode:
    def __init__(self, node_id: uuid.UUID, node_type: str, data: dict):
        self.node_id = node_id
        self.node_type = node_type
        self.data = data

class ProvenanceEdge:
    def __init__(self, source_id: uuid.UUID, target_id: uuid.UUID, relationship: str):
        self.source_id = source_id
        self.target_id = target_id
        self.relationship = relationship

class ProvenanceGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = []
        
    def add_node(self, node_id: uuid.UUID, node_type: str, data: dict):
        self.nodes[node_id] = ProvenanceNode(node_id, node_type, data)
        
    def add_edge(self, source_id: uuid.UUID, target_id: uuid.UUID, relationship: str):
        self.edges.append(ProvenanceEdge(source_id, target_id, relationship))
        
    def to_dict(self):
        return {
            "nodes": [{"id": str(n.node_id), "type": n.node_type, "data": n.data} for n in self.nodes.values()],
            "edges": [{"source": str(e.source_id), "target": str(e.target_id), "relation": e.relationship} for e in self.edges]
        }
