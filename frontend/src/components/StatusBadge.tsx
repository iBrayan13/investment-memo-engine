import type { MemoStatus } from '@/types/memo';
import { statusMap } from '@/utils/format';

const variantClasses: Record<string, string> = {
  started: 'bg-status-started-bg text-status-started-fg',
  progress: 'bg-status-progress-bg text-status-progress-fg',
  completed: 'bg-status-completed-bg text-status-completed-fg',
  failed: 'bg-status-failed-bg text-status-failed-fg',
};

export function StatusBadge({ status }: { status: MemoStatus }) {
  const info = statusMap[status] ?? { label: status, variant: 'started' as const };
  return (
    <span className={`inline-flex items-center rounded-sm px-2 py-0.5 text-xs font-medium ${variantClasses[info.variant]}`}>
      {info.label}
    </span>
  );
}
