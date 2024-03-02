'use client';
import { useState } from 'react';
import useGetDecision from '@/app/hooks/use-get-decision';
import StreamDecisionTreeJSON from '@/app/ui/stream-decision-tree-json';
import StreamDecisionTree from '@/app/ui/stream-decision-tree';

const Dashboard = () => {
  const [showJsonData, setShowJsonData] = useState<boolean>(false);

  const { loading, getDecision } = useGetDecision();

  const hideData = () => {
    setShowJsonData(false);
  }

  const showData = () => {
    setShowJsonData(true);
  }

  return (
    <div className="flex flex-col min-h-screen p-24">
      <h1 className="text-center text-xl mb-4">Dashboard</h1>

      <div className="mb-4">
        <button
          onClick={getDecision}
          disabled={loading}
          className={`${loading ? 'bg-gray-500 hover:bg-gray-300 cursor-not-allowed' : 'bg-green-500 hover:bg-green-700'} text-white font-bold py-2 px-4 rounded`}
        >
          {loading ? "Loading..." : "Get Decision"}
        </button>
        {!showJsonData && 
          <button
            onClick={showData}
            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ml-4"
          >
            Show JSON Data
          </button>
        }
        {showJsonData &&
          <button
            onClick={hideData}
            className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded ml-4"
          >
            Hide Data
          </button>
        }

        {showJsonData && <StreamDecisionTreeJSON/>}
      </div>

      <div className="flex-grow">
        <StreamDecisionTree />
      </div>
    </div>
  );
};

export default Dashboard;
