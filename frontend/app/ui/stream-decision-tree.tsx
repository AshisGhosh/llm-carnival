import React, { useState, useCallback } from 'react';
import useSSE from '@/app/lib/use-sse';
import { D3Node } from '@/app/lib/definitions';
import transformTreeForD3 from '@/app/lib/transform-data-for-d3';
import DecisionTree from './decision-tree';

export default function StreamDecisionTree() {
  const [data, setData] = useState<D3Node | null>(null);

  const handleNewData = useCallback((newData: any) => {
    if (newData["success"]){
      const transformedData = transformTreeForD3(newData['data']); // Adjust based on your actual data structure
      setData(transformedData);
    }
  }, []); // Empty dependency array means this callback never changes

  useSSE('http://localhost:8002/action_decision/stream_decision_tree', handleNewData);

  return (
    <div>
      <pre className="whitespace-pre-wrap p-4 max-w-8xl mx-auto my-8 bg-white rounded-lg shadow-lg border border-gray-200 overflow-auto overflow-x-auto">
            {data && <DecisionTree data={data}/>}
      </pre>  
    </div>
  );
}
