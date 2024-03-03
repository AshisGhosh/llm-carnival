import React, { useState, useCallback } from 'react';
import useSSE from '@/app/lib/use-sse';

export default function TimeSince() {
    const [time, setTime] = useState<number>(0);
  
    const handleNewData = useCallback((newData: any) => {
        // console.log(newData);  // Log the data for debugging
        if (newData["success"]){
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
        <span>{time && time > 0 ? `Time elapsed: ${time.toFixed(3)} ms` : '0 ms'}</span>
    );
}