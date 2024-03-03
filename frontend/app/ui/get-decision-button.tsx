import React, { useState, useCallback, useEffect } from 'react';
import useSSE from '@/app/lib/use-sse';
import useGetDecision from '@/app/hooks/use-get-decision';

export default function GetDecisionButton() {
    const [loading, setLoading] = useState<boolean>(false);
    const { loading: decisionLoading, getDecision } = useGetDecision();

    useEffect(() => {
        setLoading(decisionLoading);
    }, [decisionLoading]);
  
    const handleNewData = useCallback((newData: any) => {
        if (newData["success"]){
            if (newData["data"]["end_time"]){
                setLoading(false);
            }
            else{
                setLoading(true);
            }
        }
    }, []); // Empty dependency array means this callback never changes
  
    useSSE('http://localhost:8002/action_decision/stream_decision_tree', handleNewData);
  
    return (
        <button
          onClick={getDecision}
          disabled={loading}
          className={`${loading ? 'bg-gray-500 hover:bg-gray-300 cursor-not-allowed' : 'bg-green-500 hover:bg-green-700'} text-white font-bold py-2 px-4 rounded`}
        >
          {loading ? "Loading..." : "Get Decision"}
        </button>
    );
}