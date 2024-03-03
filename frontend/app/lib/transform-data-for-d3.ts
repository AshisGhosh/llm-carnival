import { DecisionTree, DecisionNode, D3Node } from "./definitions"; 

const transformDataForD3 = (data: DecisionNode | boolean, current_node_id: number): D3Node => {
    // Base case: if the data is not an object (e.g., true/false in your example),
    // return an object with a name property.
    if (typeof data !== 'object') {
        return { name: data.toString(), id: 0, is_current_node: true};
    }
    
    // Transform the current object and recursively transform its children.
    let transformed: D3Node = {
        id: data.id,
        name: data.decision || 'Root', // Use 'Root' as a fallback name
        is_current_node: data.id === current_node_id,
        children: data.children ? data.children.map(child => transformDataForD3(child, current_node_id)) : []
    };
  
    return transformed;
  }

const transformTreeDataForD3 = (data: DecisionTree): D3Node => {
    return transformDataForD3(data.tree, data.current_node_id);
  }

export default transformTreeDataForD3;

  