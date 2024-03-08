import React, { useState, useCallback } from 'react';
import useFetchImage from '@/app/hooks/fetch-image';

export default function ImageHandler() {
    const [showImage, setShowImage] = useState<boolean>(false);
    const { loading, imageUrl, fetchImage } = useFetchImage();

    const refreshImage = () => {
        console.log('refreshing image');
        fetchImage();
    }

    // Drag state to change the UI accordingly
    const [isDragging, setIsDragging] = useState(false);

    // Prevent default behavior for drag and drop
    const preventDefaults = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    // Highlight drop area when item is dragged over it
    const handleDragEnter = useCallback((e) => {
        preventDefaults(e);
        setIsDragging(true);
    }, []);

    // Unhighlight drop area when item leaves it
    const handleDragLeave = useCallback((e) => {
        preventDefaults(e);
        setIsDragging(false);
    }, []);

    // Handle the drop event
    const handleDrop = useCallback((e) => {
        preventDefaults(e);
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            // Assuming you have an endpoint to handle the file upload
            const file = e.dataTransfer.files[0];
            // Implement the logic to send the file to your server
            uploadImage(file);
        }
    }, []);

    // Function to upload image
    const uploadImage = async (file) => {
        const formData = new FormData();
        formData.append('image', file);

        try {
            await fetch('http://localhost:8000/game_state/update_image', {
                method: 'POST',
                body: formData,
            });
            fetchImage(); // Refresh the image after upload
        } catch (error) {
            console.error('Error uploading the image:', error);
        }
    };

    return(
        <div className={`flex flex-col mb-4 ${isDragging ? 'dragging bg-yellow-300' : ''}`}
            onDragEnter={handleDragEnter}
            onDragOver={preventDefaults} // Necessary to allow drop
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}>
            <div className='flex flex-row mb-4'>
                <button
                    onClick={() => setShowImage(!showImage)}
                    className={`${showImage ? 'bg-red-500 hover:bg-red-700' : 'bg-green-500 hover:bg-green-700'} text-white font-bold py-2 px-4 rounded`}>
                    {showImage ? "Hide" : "Show" } Image
                </button>
                <button
                    onClick={refreshImage}
                    className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded ml-4">
                    Refresh Image
                </button>
            </div>
            {showImage &&
                <div className="whitespace-pre-wrap p-4 max-w-8xl mx-auto mb-8 bg-white rounded-lg shadow-lg border border-gray-200 overflow-auto overflow-x-auto">
                    <img src={imageUrl} alt="Image from the server" />
                </div>
            }
        </div>
    );
}