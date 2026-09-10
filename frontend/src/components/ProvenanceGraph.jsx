import React, { useMemo } from 'react';
import { ReactFlow, Background, Controls, MiniMap } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

export default function ProvenanceGraph({ result }) {
  const { nodes, edges } = useMemo(() => {
    const initialNodes = [];
    const initialEdges = [];

    // Query Node
    initialNodes.push({
      id: 'query',
      position: { x: 250, y: 0 },
      data: { label: 'Query' },
      style: { background: '#f8fafc', border: '2px solid #94a3b8', borderRadius: '8px', padding: '10px' }
    });

    // Answer Node
    initialNodes.push({
      id: 'answer',
      position: { x: 250, y: 100 },
      data: { label: 'AI Answer' },
      style: { background: '#e0f2fe', border: '2px solid #38bdf8', borderRadius: '8px', padding: '10px' }
    });
    initialEdges.push({ id: 'e-q-a', source: 'query', target: 'answer', animated: true });

    // Claim Nodes
    if (result && result.claims && result.claims.details) {
      result.claims.details.forEach((claim, index) => {
        const claimId = `claim-${index}`;
        let bgColor = '#f1f5f9';
        let borderColor = '#cbd5e1';
        
        if (claim.status === 'SUPPORTED') {
          bgColor = '#dcfce7'; borderColor = '#22c55e';
        } else if (claim.status === 'REFUTED') {
          bgColor = '#fee2e2'; borderColor = '#ef4444';
        }

        initialNodes.push({
          id: claimId,
          position: { x: index * 250, y: 250 },
          data: { label: claim.text.substring(0, 40) + '...' },
          style: { background: bgColor, border: `2px solid ${borderColor}`, borderRadius: '8px', padding: '10px', fontSize: '12px', width: 200 }
        });
        
        initialEdges.push({ id: `e-a-${claimId}`, source: 'answer', target: claimId });
      });
    }

    return { nodes: initialNodes, edges: initialEdges };
  }, [result]);

  return (
    <div style={{ width: '100%', height: '400px', border: '1px solid #e2e8f0', borderRadius: '12px', overflow: 'hidden' }}>
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background color="#ccc" gap={16} />
        <Controls />
        <MiniMap />
      </ReactFlow>
    </div>
  );
}
