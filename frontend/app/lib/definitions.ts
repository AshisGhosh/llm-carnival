export interface DecisionNode {
    id: number;
    decision: string;
    depth: number;
    children?: DecisionNode[];
  }

export interface DecisionTree{
    tree: DecisionNode;
    current_node_id: number;
    current_node_desc: string;
    current_step: string;
    start_time: number;
}

export interface D3Node {
    id: number;
    name: string;
    is_current_node: boolean;
    children?: D3Node[];
  }