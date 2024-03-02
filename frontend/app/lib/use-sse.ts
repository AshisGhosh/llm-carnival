import { useEffect } from "react";

const useSSE = (url: string, callback: (data: any) => void) => {
    useEffect(() => {
      if (typeof window !== "undefined") { 
          console.log('Attempting to open SSE connection to', url);
          const eventSource = new EventSource(url);
  
          eventSource.onopen = (event) => {
              console.log('SSE connection opened', event);
          };
  
          eventSource.onmessage = (event) => {
              console.log('SSE message received', event.data);
              const data = JSON.parse(event.data);
              callback(data);
          };
  
          eventSource.onerror = (error) => {
              console.error('SSE error', error);
              if (eventSource.readyState === EventSource.CLOSED) {
                  console.log('SSE connection was closed');
              }
              eventSource.close();
          };
  
          return () => {
              console.log('Closing SSE connection');
              eventSource.close();
          };
      }
    }, [url, callback]); // Dependency array to re-run the effect if url or callback changes
};

export default useSSE;