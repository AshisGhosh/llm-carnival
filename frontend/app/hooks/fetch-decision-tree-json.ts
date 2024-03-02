import { useState } from 'react';
import { DecisionNode } from '@/app/lib/definitions';

const api_url = 'http://localhost:8002/action_decision/get_decision_tree';

const useFetchDecisionTreeJson = () => {
    const [treeData, setTreeData] = useState<DecisionNode | null>(null);
    const [currentNodeID, setCurrentNodeID] = useState<number | null>(null);
    const [currentNodeDesc, setCurrentNodeDesc] = useState<string | null>(null);
    const [currentStep, setCurrentStep] = useState<string | null>(null);
    const [startTime, setStartTime] = useState<number | null>(null);

    const fetchData = async () => {
        try {
            const response = await fetch(api_url);
            if (!response.ok) throw new Error('Network response was not ok');
            const tree_data = await response.json();
            if (tree_data["success"]){
                setTreeData(tree_data["data"]["tree"]);
                setCurrentNodeID(tree_data["data"]["current_node_id"]);
                setCurrentNodeDesc(tree_data["data"]["current_node_desc"]);
                setCurrentStep(tree_data["data"]["current_step"]);
                setStartTime(tree_data["data"]["start_time"]);
            }
            else{
                throw new Error('No data');
            }
            
        } catch (error) {
            console.error(error);
        }
    };

    return { treeData, currentNodeID, currentNodeDesc, currentStep, startTime, fetchData };
}

export default useFetchDecisionTreeJson;
