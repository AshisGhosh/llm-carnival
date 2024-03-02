export interface DecisionNode {
    id: number;
    decision: string;
    depth: number;
    children?: DecisionNode[];
  }

export interface D3Node {
    name: string;
    children?: D3Node[];
  }