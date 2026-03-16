export const formatCurrency = (value: number): string =>
  new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'USD' }).format(value);

export const formatPercent = (value: number): string =>
  `${(value * 100).toFixed(1)}%`;

export const formatNumber = (value: number): string =>
  new Intl.NumberFormat('es-MX').format(value);

export const statusMap: Record<string, { label: string; variant: 'started' | 'progress' | 'completed' | 'failed' }> = {
  started: { label: 'Iniciado', variant: 'started' },
  in_progress: { label: 'En progreso', variant: 'progress' },
  completed: { label: 'Completado', variant: 'completed' },
  failed: { label: 'Fallido', variant: 'failed' },
};
