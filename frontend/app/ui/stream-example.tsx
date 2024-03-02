import React, { useState, useCallback } from 'react';
import useSSE from '@/app/lib/use-sse';

export default function StreamExample() {
  const [data, setData] = useState(null);

  const handleNewData = useCallback((newData: any) => {
    console.log(newData);  // Log the data for debugging
    setData(newData); // Update the state with the new data
  }, []); // Empty dependency array means this callback never changes

  useSSE('http://localhost:8002/stream_example', handleNewData);

  return (
    <div>
      Check the console for updates. {data && JSON.stringify(data)}
    </div>
  );
}
