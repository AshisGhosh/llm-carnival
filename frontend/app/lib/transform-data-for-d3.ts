import { DecisionNode, D3Node } from "./definitions"; 

const transformDataForD3 = (data: DecisionNode | boolean): D3Node => {
    // Base case: if the data is not an object (e.g., true/false in your example),
    // return an object with a name property.
    if (typeof data !== 'object') {
        return { name: data.toString() };
    }
  
    // Transform the current object and recursively transform its children.
    let transformed: D3Node = {
        name: data.decision || 'Root', // Use 'Root' as a fallback name
        children: data.children ? data.children.map(child => transformDataForD3(child)) : []
    };
  
    return transformed;
}

export default transformDataForD3;

  