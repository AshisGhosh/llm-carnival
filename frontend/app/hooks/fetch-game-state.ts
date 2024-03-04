import { useState } from 'react';

const api_url = 'http://localhost:8002/action_decision/get_game_state';

const useFetchGameState = () => {
    const [data, setData] = useState(null);

    const fetchData = async () => {
        try {
            const response = await fetch(api_url);
            if (!response.ok) throw new Error('Network response was not ok');
            const gameState = await response.json();
            setData(gameState);
        } catch (error) {
            console.error(error);
        }
    };

    return { data, fetchData };
};

export default useFetchGameState;