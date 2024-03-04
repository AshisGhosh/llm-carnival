import React, { useState, useCallback } from 'react';
import useSSE from '@/app/lib/use-sse';

export default function StreamDecisionTreeCurrentStep() {
  const [data, setData] = useState(null);
  const [time, setTime] = useState(0);

  const handleNewData = useCallback((newData: any) => {
    if (newData["success"]){
      // console.log(newData["data"]["current_step"]);  // Log the data for debugging (optional
      setData(newData["data"]["current_step"]); // Update the state with the new data
      if (newData["data"]["end_time"]){
        setTime(newData["data"]["end_time"] - newData["data"]["start_time"]);
      }
      else{
        setTime(new Date().getTime()/1000 - newData["data"]["start_time"]);
      }      
    }
  }, []); // Empty dependency array means this callback never changes

  useSSE('http://localhost:8002/action_decision/stream_decision_tree', handleNewData);

  return (
    <div>
      <pre className="whitespace-pre-wrap p-4 max-w-8xl mx-auto my-8 bg-white rounded-lg shadow-lg border border-gray-200 overflow-auto overflow-x-auto">
        <span>{time && time > 0 ? `Time elapsed: ${time.toFixed(3)} ms` : '0 ms'}</span>    
        <br />
        <span>{data && data}</span>
      </pre>  
    </div>
  );
}
