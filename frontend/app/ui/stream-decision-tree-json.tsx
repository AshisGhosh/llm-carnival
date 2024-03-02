import React, { useState, useCallback } from 'react';
import useSSE from '@/app/lib/use-sse';

export default function StreamDecisionTreeJSON() {
  const [data, setData] = useState(null);

  const handleNewData = useCallback((newData: any) => {
    setData(newData); // Update the state with the new data
  }, []); // Empty dependency array means this callback never changes

  useSSE('http://localhost:8002/action_decision/stream_decision_tree', handleNewData);

  return (
    <div>
      <pre className="whitespace-pre-wrap p-4 max-w-8xl mx-auto my-8 bg-white rounded-lg shadow-lg border border-gray-200 overflow-auto overflow-x-auto">
            {data && JSON.stringify(data, null, 2)}
      </pre>  
    </div>
  );
}
