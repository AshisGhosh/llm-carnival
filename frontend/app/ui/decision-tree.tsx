import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { D3Node } from '@/app/lib/definitions';
import { HierarchyPointNode } from 'd3';

interface DecisionTreeProps {
  data: D3Node;
}

const DecisionTree: React.FC<DecisionTreeProps> = ({ data }) => {
  const d3Container = useRef<SVGSVGElement | null>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [lastDimensions, setLastDimensions] = useState({ width: 0, height: 0 });

  const drawTree = (width: number, height: number) => {
    if (!data || !d3Container.current) return;

    const margin = { top: 20, right: 120, bottom: 30, left: 180 };
    const adjustedWidth = width - margin.left - margin.right;
    const adjustedHeight = height - margin.top - margin.bottom;

    // Clear the container
    d3.select(d3Container.current).selectAll("*").remove();

    const svg = d3.select(d3Container.current)
        .attr('width', width + margin.right + margin.left)
        .attr('height', height + margin.top + margin.bottom)
      .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const treemap = d3.tree<D3Node>().size([adjustedHeight, adjustedWidth]);
    const root = d3.hierarchy(data, (d: D3Node) => d.children) as HierarchyPointNode<D3Node>;

    treemap(root);

    // Add links between nodes
    svg.selectAll('.link')
    .data(root.descendants().slice(1))
  .enter().append('path')
    .attr('class', 'link')
    .style('stroke-width', '2px') // Set the thickness of the link
    .style('stroke', 'black') // Set the color of the link
    .style('fill', 'none') // Remove the fill
    .attr('d', d => {
        const o = {x: d.x, y: d.y};
        const p = {x: d.parent?.x ?? 0, y: d.parent?.y ?? 0};
        return `M${o.y},${o.x}C${(o.y + p.y) / 2},${o.x} ${(o.y + p.y) / 2},${p.x} ${p.y},${p.x}`;
    });

    // Add nodes
    const node = svg.selectAll('.node')
        .data(root.descendants())
      .enter().append('g')
        .attr('class', (d: HierarchyPointNode<D3Node>) => `node ${d.children ? ' node--internal' : ' node--leaf'}`)
        .attr('transform', (d: HierarchyPointNode<D3Node>) => `translate(${d.y},${d.x})`);

    // node.append('circle')
    //     .attr('r', 10);
    
    const charsPerRow = 22
    const rowHeight = 28 // Adjust based on your font size and line-height
    node.append('foreignObject')
      .attr('class', 'svg-content') // Add a class
      .attr('class', 'text-white bg-black rounded-lg p-2 shadow') // Add a class
      .attr('width', 200) // Set a fixed width for text wrapping
      .attr('height', d => {
        const textLength = d.data.name.length;
        const numRows = Math.ceil(textLength / charsPerRow);
        const padding = 4; // Add some padding
        return numRows * rowHeight + padding; // Total height based on text length
      })
      .attr('x', -100) // Adjust based on text length
      .attr('y', d => {
        const textLength = d.data.name.length;
        const numRows = Math.ceil(textLength / charsPerRow);
        const padding = 4; // Add some padding
        return -(numRows * rowHeight + padding) / 2; // Center the text vertically
      })
      .html(d => `${d.data.name}`); // Your HTML content
    
  };

  useEffect(() => {
    const resizeObserver = new ResizeObserver(entries => {
      if (!entries || entries.length === 0) return;
      const { width, height } = entries[0].contentRect;

      // Check if the resize is significant
      // if (Math.abs(lastDimensions.width - width) > 10 || Math.abs(lastDimensions.height - height) > 10) {
      if (true) {
        drawTree(width, height);
        setLastDimensions({ width, height });
      }
    });

    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }

    return () => {
      if (containerRef.current) {
        resizeObserver.unobserve(containerRef.current);
      }
    };
  }, [data, lastDimensions]); // Redraw when data or dimensions change

  useEffect(() => {
    // Initial draw with default dimensions
    if (containerRef.current) {
      const { clientWidth, clientHeight } = containerRef.current;
      drawTree(clientWidth, clientHeight);
      setLastDimensions({ width: clientWidth, height: clientHeight });
    }
  }, []); // Only on initial mount

  return (
    <div ref={containerRef} style={{ width: '100%', height: '100%', maxHeight: '1000px', overflow: 'auto' }}>
      <svg ref={d3Container} width="100%" height="100%" />
    </div>
  );
};

export default DecisionTree;