import React, { useState, useCallback } from 'react';
import useSSE from '@/app/lib/use-sse';

export default function StreamGameAnalyzerStatus() {
  const [data, setData] = useState(null);
  const [time, setTime] = useState(0);

  const handleNewData = useCallback((newData: any) => {
    if (newData["start_time"]){
      setData(newData["analyzer_status"]);
      if (newData["end_time"]){
        setTime(newData["end_time"] - newData["start_time"]);
      }
      else{
        setTime(new Date().getTime()/1000 - newData["start_time"]);
      }
    }
  }, []); // Empty dependency array means this callback never changes

  useSSE('http://localhost:8000/game_state/stream_analyzer_status', handleNewData);

  return (
    <div>
      <pre className="whitespace-pre-wrap p-4 max-w-8xl mx-auto mt-4 mb-8 bg-white rounded-lg shadow-lg border border-gray-200 overflow-auto overflow-x-auto">
        <span>{time && time > 0 ? `Time elapsed: ${time.toFixed(3)} ms` : '0 ms'}</span>
        <br />
        <span>{data}</span>
      </pre>  
    </div>
  );
}
