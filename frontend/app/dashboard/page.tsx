'use client';
import { useState } from 'react';
import StreamDecisionTreeJSON from '@/app/ui/stream-decision-tree-json';
import StreamDecisionTree from '@/app/ui/stream-decision-tree';
import StreamDecisionTreeCurrentStep from '@/app/ui/stream-decision-tree-current-step';
import { GameState } from '@/app/ui/game-state';
import GetDecisionButton from '@/app/ui/get-decision-button';
import StreamGameAnalyzerStatus from '@/app/ui/stream-game-analyzer-status';
import ImageHandler from '@/app/ui/image-handler';

const Dashboard = () => {
  const [showJsonData, setShowJsonData] = useState<boolean>(false);

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
        <ImageHandler />
        <GameState />
        <StreamGameAnalyzerStatus />
        <GetDecisionButton />
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
        <StreamDecisionTreeCurrentStep />
        {showJsonData && <StreamDecisionTreeJSON/>}
      </div>

      <div className="flex-grow">
        <StreamDecisionTree />
      </div>
    </div>
  );
};

export default Dashboard;
