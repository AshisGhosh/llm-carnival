import React, { useState, useCallback } from 'react';
import useSSE from '@/app/lib/use-sse';
import { D3Node } from '@/app/lib/definitions';
import transformTreeForD3 from '@/app/lib/transform-data-for-d3';
import DecisionTree from './decision-tree';

export default function StreamDecisionTree() {
  const [data, setData] = useState<D3Node | null>(null);
  const [time, setTime] = useState<number>(0);


  const handleNewData = useCallback((newData: any) => {
    if (newData["success"]){
      const transformedData = transformTreeForD3(newData['data']); // Adjust based on your actual data structure
      setData(transformedData);
      if (newData["success"]){
        if (newData["data"]["end_time"]){
            setTime(newData["data"]["end_time"] - newData["data"]["start_time"]);
        }
        else{
            setTime(new Date().getTime()/1000 - newData["data"]["start_time"]);
        }
    }
    }
  }, []); // Empty dependency array means this callback never changes

  useSSE('http://localhost:8002/action_decision/stream_decision_tree', handleNewData);

  return (
    <div>
      <pre className="whitespace-pre-wrap p-4 max-w-8xl mx-auto mb-8 bg-white rounded-lg shadow-lg border border-gray-200 overflow-auto overflow-x-auto">
        <span>{time && time > 0 ? `Time elapsed: ${time.toFixed(3)} ms` : '0 ms'}</span>
            {data && <DecisionTree data={data}/>}
      </pre>  
    </div>
  );
}
