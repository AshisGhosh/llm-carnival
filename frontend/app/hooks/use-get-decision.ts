import { useState } from 'react';

const api_url = 'http://localhost:8002/action_decision/get_decision';

const useGetDecision = () => {
    const [loading, setLoading] = useState<boolean>(false);

    const getDecision = async () => {
        setLoading(true);
        try {
            const response = await fetch(api_url);
            if (!response.ok) throw new Error('Network response was not ok');
            const responseJson = await response.json();
            if (!responseJson[0]) throw new Error('No data');
            console.log(responseJson);
            
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return { loading, getDecision };
}

export default useGetDecision;
