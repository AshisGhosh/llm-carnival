import { useState } from 'react';

const api_url = 'http://localhost:8000/game_state/update_game_state';

const useUpdateGameState = () => {
    const [loading, setLoading] = useState<boolean>(false);

    const updateGameState = async () => {
        setLoading(true);
        try {
            const response = await fetch(api_url);
            if (!response.ok) throw new Error('Network response was not ok');
            const responseJson = await response.json();
            if (!responseJson["success"]) throw new Error('No data');
            console.log(responseJson);
            
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return { loading, updateGameState };
}

export default useUpdateGameState;
