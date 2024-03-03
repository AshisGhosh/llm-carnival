import { useEffect, useState } from 'react';
import { D3Node } from '@/app/lib/definitions';
import transformTreeforD3 from '@/app/lib/transform-data-for-d3';

const api_url = 'http://localhost:8002/action_decision/get_decision_tree';

const useFetchDecisionTree = () => {
  const [data, setData] = useState<D3Node | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchData = async () => {
    // If there is no data yet, set loading to true
    if (!data) setLoading(false);
    try {
      const response = await fetch(api_url);
      if (!response.ok) throw new Error('Network response was not ok');
      const treeData = await response.json();
      if (!treeData['data']) throw new Error('No data');
      const transformedData = transformTreeforD3(treeData['data']); // Adjust based on your actual data structure
      setData(transformedData);
    } catch (error) {
      if (error instanceof Error) setError(error);
      else setError(new Error('An error occurred'));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 500);
    return () => clearInterval(interval);
  }, []);

  return { data, loading, error };
};

export default useFetchDecisionTree;
