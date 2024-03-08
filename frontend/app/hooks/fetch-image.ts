import { useState } from 'react';

const api_url = 'http://localhost:8000/game_state/get_image';

const useFetchImage = () => {
    const [loading, setLoading] = useState(false);
    const [imageUrl, setImageUrl] = useState<string>();

    const fetchImage = async () => {
        setLoading(true);
        try {
            const response = await fetch(api_url);
            if (!response.ok) throw new Error('Network response was not ok');
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            setImageUrl(url);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    return { loading, imageUrl, fetchImage };
}

export default useFetchImage;