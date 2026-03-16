import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { MemoService } from '@/services/api';
import { StatusBadge } from '@/components/StatusBadge';
import { TableSkeleton } from '@/components/TableSkeleton';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search, Plus, Eye, Trash2, ChevronLeft, ChevronRight } from 'lucide-react';
import { toast } from 'sonner';
import type { Memo } from '@/types/memo';

const ITEMS_PER_PAGE = 10;

export default function Dashboard() {
  const navigate = useNavigate();
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);

  const { data: memos = [], isLoading, isError, refetch } = useQuery({
    queryKey: ['memos'],
    queryFn: () => MemoService.getAll(),
    refetchInterval: 15000,
  });

  const handleDelete = useCallback(async (id: string) => {
    if (!window.confirm('¿Estás seguro de eliminar este memorando?')) return;
    try {
      await MemoService.delete(id);
      toast.success('Memorando eliminado');
      refetch();
    } catch {
      toast.error('Error al eliminar el memorando');
    }
  }, [refetch]);

  const filtered = memos.filter((m: Memo) => {
    if (!search) return true;
    const name = m.memo_object?.investment_memo?.project_name?.toLowerCase() ?? '';
    return name.includes(search.toLowerCase());
  });

  const totalPages = Math.max(1, Math.ceil(filtered.length / ITEMS_PER_PAGE));
  const paginated = filtered.slice((page - 1) * ITEMS_PER_PAGE, page * ITEMS_PER_PAGE);

  const getValue = (m: Memo, field: 'project_name' | 'location' | 'asset_type') =>
    m.status === 'completed' && m.memo_object?.investment_memo
      ? m.memo_object.investment_memo[field]
      : '—';

  return (
    <div className="min-h-screen bg-surface-elevated">
      <div className="mx-auto max-w-7xl px-6 py-8">
        {/* Header */}
        <div className="mb-6 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Memorandos de Inversión</h1>
            <p className="mt-1 text-sm text-muted-foreground">
              {memos.length} memorando{memos.length !== 1 ? 's' : ''} en total
            </p>
          </div>
          <Button
            onClick={() => navigate('/generate')}
            className="gap-2"
          >
            <Plus className="h-4 w-4" />
            Generar Memorando
          </Button>
        </div>

        {/* Search */}
        <div className="mb-4">
          <div className="relative max-w-sm">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <Input
              placeholder="Buscar por proyecto..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setPage(1); }}
              className="pl-9 text-sm"
            />
          </div>
        </div>

        {/* Table */}
        <div className="overflow-hidden rounded-lg bg-card shadow-card">
          {isLoading ? (
            <TableSkeleton />
          ) : isError ? (
            <div className="flex flex-col items-center justify-center py-16 text-muted-foreground">
              <p className="mb-2 text-sm">Error al cargar los memorandos</p>
              <Button variant="outline" size="sm" onClick={() => refetch()}>
                Reintentar
              </Button>
            </div>
          ) : filtered.length === 0 ? (
            <div className="py-16 text-center text-sm text-muted-foreground">
              {search ? 'No se encontraron resultados' : 'No hay memorandos aún'}
            </div>
          ) : (
            <>
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border bg-muted/50">
                      <th className="px-4 py-3 text-left font-medium text-muted-foreground">ID</th>
                      <th className="px-4 py-3 text-left font-medium text-muted-foreground">Proyecto</th>
                      <th className="px-4 py-3 text-left font-medium text-muted-foreground">Ubicación</th>
                      <th className="px-4 py-3 text-left font-medium text-muted-foreground">Tipo de Activo</th>
                      <th className="px-4 py-3 text-left font-medium text-muted-foreground">Estado</th>
                      <th className="px-4 py-3 text-left font-medium text-muted-foreground">Mensaje</th>
                      <th className="px-4 py-3 text-right font-medium text-muted-foreground">Acciones</th>
                    </tr>
                  </thead>
                  <tbody>
                    {paginated.map((m: Memo) => (
                      <tr
                        key={m.memo_id}
                        className="border-b border-border transition-colors duration-150 last:border-0 hover:bg-muted/30"
                      >
                        <td className="px-4 py-3 font-mono text-xs text-muted-foreground">
                          {m.memo_id.length > 16 ? `${m.memo_id.slice(0, 16)}…` : m.memo_id}
                        </td>
                        <td className="px-4 py-3 font-medium">{getValue(m, 'project_name')}</td>
                        <td className="px-4 py-3 text-muted-foreground">{getValue(m, 'location')}</td>
                        <td className="px-4 py-3 text-muted-foreground">{getValue(m, 'asset_type')}</td>
                        <td className="px-4 py-3">
                          <StatusBadge status={m.status} />
                        </td>
                        <td className="max-w-[200px] truncate px-4 py-3 text-muted-foreground">
                          {m.status_message || '—'}
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex items-center justify-end gap-1">
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-8 gap-1.5 text-xs"
                              onClick={() => navigate(`/memo/${m.memo_id}`)}
                            >
                              <Eye className="h-3.5 w-3.5" />
                              Ver
                            </Button>
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-8 gap-1.5 text-xs text-destructive hover:text-destructive"
                              onClick={() => handleDelete(m.memo_id)}
                            >
                              <Trash2 className="h-3.5 w-3.5" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-between border-t border-border px-4 py-3">
                  <span className="text-xs text-muted-foreground">
                    Mostrando {(page - 1) * ITEMS_PER_PAGE + 1}–{Math.min(page * ITEMS_PER_PAGE, filtered.length)} de {filtered.length}
                  </span>
                  <div className="flex items-center gap-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      disabled={page <= 1}
                      onClick={() => setPage(p => p - 1)}
                    >
                      <ChevronLeft className="h-4 w-4" />
                    </Button>
                    <span className="px-2 text-xs text-muted-foreground">
                      {page} / {totalPages}
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      disabled={page >= totalPages}
                      onClick={() => setPage(p => p + 1)}
                    >
                      <ChevronRight className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
}
