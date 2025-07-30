declare module 'react-chartjs-2' {
  import { Component } from 'react';
  import { ChartData, ChartOptions } from 'chart.js';

  export interface LineProps {
    data: ChartData<'line'>;
    options?: ChartOptions<'line'>;
  }

  export interface PieProps {
    data: ChartData<'pie'>;
    options?: ChartOptions<'pie'>;
  }

  export class Line extends Component<LineProps> {}
  export class Pie extends Component<PieProps> {}
} 