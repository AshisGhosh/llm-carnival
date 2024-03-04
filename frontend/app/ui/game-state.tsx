import useFetchGameState from "@/app/hooks/fetch-game-state";
import { useState, useEffect } from "react";
import { remark } from 'remark';
import html from 'remark-html';
import useUpdateGameState from "@/app/hooks/use-update-game-state";

export function GameState() {
    const [showData, setShowData] = useState<boolean>(false);
    const { data, fetchData } = useFetchGameState();
    const [processedData, setProcessedData] = useState<string>("");
    const { loading, updateGameState } = useUpdateGameState();

    const getData = () => {
        fetchData();
        setShowData(true);
    }

    const hideData = () => {
        setShowData(false);
    }

    useEffect(() => {
        if (!data) return;
        // Define an async function inside useEffect
        const processContent = async () => {
            const processedContent = await remark()
                .use(html)
                .process(data["summary"]);
            const contentHtml = processedContent.toString();
            setProcessedData(contentHtml);
        };

        // Call the async function
        processContent();
    }, [data]);

    
    return (
        <div className="flex-col">
            {!showData &&
                <button
                    onClick={getData}
                    className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded mb-4"
                >
                    Show Game State
                </button>
            }
            {showData &&
                <button
                    onClick={hideData}
                    className="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded mb-4"
                >
                    Hide Game State
                </button>
            }
            <button
                onClick={updateGameState}
                disabled={loading}
                className={`${loading ? 'bg-gray-500 hover:bg-gray-300 cursor-not-allowed' : 'bg-blue-500 hover:bg-blue-700'} text-white font-bold py-2 px-4 rounded ml-4`}
            >
                {loading ? "Loading..." : "Update Game State"}
            </button>
            { showData && data &&
                <div className="whitespace-pre-wrap p-4 max-w-8xl mx-auto my-8 bg-white rounded-lg shadow-lg border border-gray-200 overflow-auto overflow-x-auto">
                   <div dangerouslySetInnerHTML={{ __html: processedData }} />
                </div>
            }
            
            {showData && <pre className="whitespace-pre-wrap p-4 max-w-8xl mx-auto my-8 bg-white rounded-lg shadow-lg border border-gray-200 overflow-auto overflow-x-auto">{JSON.stringify(data, null, 2)}</pre>}
        </div>
    );
}
