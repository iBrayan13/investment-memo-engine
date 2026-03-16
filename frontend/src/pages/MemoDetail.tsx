import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { MemoService } from '@/services/api';
import { StatusBadge } from '@/components/StatusBadge';
import { Button } from '@/components/ui/button';
import { Skeleton } from '@/components/ui/skeleton';
import { toast } from 'sonner';
import { ArrowLeft, FileText, Download, Trash2, Loader2 } from 'lucide-react';
import type { Memo, MemoObject } from '@/types/memo';
import { DeleteModal } from '@/components/DeleteModal';

const API_BASE = 'http://localhost:7070';

export default function MemoDetail() {
  const { memo_id } = useParams<{ memo_id: string }>();
  const navigate = useNavigate();
  const [memo, setMemo] = useState<Memo | null>(null);
  const [loading, setLoading] = useState(true);
  const [deleteOpen, setDeleteOpen] = useState(false);

  useEffect(() => {
    if (!memo_id) return;
    let active = true;

    const fetchMemo = async () => {
      try {
        const data = await MemoService.getById(memo_id);
        if (active) { setMemo(data); setLoading(false); }
      } catch {
        if (active) { setLoading(false); toast.error('Error al cargar el memorando'); }
      }
    };

    fetchMemo();

    const interval = setInterval(() => {
      if (memo?.status === 'completed' || memo?.status === 'failed') return;
      fetchMemo();
    }, 5000);

    return () => { active = false; clearInterval(interval); };
  }, [memo_id, memo?.status]);

  const handleDelete = async () => {
    if (!memo_id) return;
    try {
      await MemoService.delete(memo_id);
      toast.success('Memorando eliminado');
      navigate('/');
    } catch {
      toast.error('Error al eliminar');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-surface-elevated">
        <div className="mx-auto max-w-5xl px-6 py-8">
          <Skeleton className="mb-4 h-8 w-64" />
          <Skeleton className="mb-2 h-4 w-48" />
          <div className="mt-8 space-y-6">
            <Skeleton className="h-40 w-full rounded-lg" />
            <Skeleton className="h-40 w-full rounded-lg" />
          </div>
        </div>
      </div>
    );
  }

  if (!memo) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-surface-elevated">
        <p className="text-sm text-muted-foreground">Memorando no encontrado</p>
      </div>
    );
  }

  const isComplete = memo.status === 'completed' && memo.memo_object;

  return (
    <div className="min-h-screen bg-surface-elevated">
      <div className="mx-auto max-w-5xl px-6 py-8">
        <Button variant="ghost" size="sm" className="mb-6 gap-2 text-muted-foreground" onClick={() => navigate('/')}>
          <ArrowLeft className="h-4 w-4" /> Volver al Dashboard
        </Button>

        <div className="mb-6 flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-foreground">Detalle del Memorando</h1>
            <p className="mt-1 font-mono text-xs text-muted-foreground">{memo.memo_id}</p>
          </div>
          <div className="flex items-center gap-2">
            <StatusBadge status={memo.status} />
            <Button variant="outline" size="sm" className="gap-1.5 text-destructive" onClick={() => setDeleteOpen(true)}>
              <Trash2 className="h-3.5 w-3.5" /> Eliminar
            </Button>
          </div>
        </div>

        {!isComplete ? (
          <div className="rounded-lg bg-card p-8 shadow-card">
            <div className="flex flex-col items-center gap-4 text-center">
              <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
              <div>
                <p className="font-medium">Estado: <StatusBadge status={memo.status} /></p>
                <p className="mt-2 text-sm text-muted-foreground">{memo.status_message || 'Procesando...'}</p>
              </div>
              <p className="text-xs text-muted-foreground">Se actualiza automáticamente cada 5 segundos</p>
            </div>
          </div>
        ) : (
          <MemoContent memoObj={memo.memo_object!} filePath={memo.memo_file_path} memoId={memo.memo_id} />
        )}
      </div>

      <DeleteModal open={deleteOpen} onClose={() => setDeleteOpen(false)} onConfirm={handleDelete} />
    </div>
  );
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="rounded-lg bg-card p-6 shadow-card">
      <h2 className="mb-4 text-base font-semibold text-foreground">{title}</h2>
      {children}
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string | number }) {
  return (
    <div className="flex items-baseline justify-between border-b border-border py-2 last:border-0">
      <span className="text-sm text-muted-foreground">{label}</span>
      <span className="text-sm font-medium">{value || '—'}</span>
    </div>
  );
}

function MemoContent({ memoObj, filePath, memoId }: { memoObj: MemoObject; filePath?: string; memoId: string }) {
  const core = memoObj.investment_memo;

  return (
    <div className="space-y-6">
      {/* Documents */}
      {filePath && (
        <div className="flex items-center gap-3 rounded-lg bg-card p-4 shadow-card">
          <FileText className="h-5 w-5 text-muted-foreground" />
          <span className="flex-1 text-sm font-medium">Documento generado</span>
          <Button variant="outline" size="sm" className="gap-1.5" asChild>
            <a href={`${API_BASE}/memo/docx/${memoId}`} download>
              <Download className="h-3.5 w-3.5" /> Descargar DOCX
            </a>
          </Button>
        </div>
      )}

      {/* 1. General Info */}
      <div className="grid gap-6 md:grid-cols-2">
        <Section title="Información General">
          <InfoRow label="Proyecto" value={core.project_name} />
          <InfoRow label="Ubicación" value={core.location} />
          <InfoRow label="Tipo de Activo" value={core.asset_type} />
          <InfoRow label="Estructura del Deal" value={core.deal_structure} />
          <InfoRow label="Preparado por" value={memoObj.prepared_by} />
          <InfoRow label="Fecha" value={memoObj.date} />
          <InfoRow label="Recomendación" value={memoObj.recommendation} />
          <InfoRow label="Costo Total (MM COP)" value={memoObj.total_project_cost} />
          <InfoRow label="Equity Requerido (MM COP)" value={memoObj.equity_required} />
        </Section>

        <Section title="Información del Activo">
          <InfoRow label="Área (m²)" value={memoObj.asset?.area_m2 ?? '—'} />
          <InfoRow label="Unidades" value={memoObj.asset?.units ?? '—'} />
          <InfoRow label="Zonificación" value={memoObj.asset?.zoning ?? '—'} />
          <InfoRow label="Año de construcción" value={memoObj.asset?.year_built ?? '—'} />
          <InfoRow label="Estado" value={memoObj.asset?.status ?? '—'} />
          <InfoRow label="Ocupación" value={memoObj.asset?.occupancy ?? '—'} />
        </Section>
      </div>

      {/* 2. Executive Summary */}
      <Section title="Resumen Ejecutivo">
        <p className="text-sm leading-relaxed text-foreground">{memoObj.executive_summary}</p>
      </Section>

      {/* 3. Highlights */}
      {memoObj.highlights?.length > 0 && (
        <Section title="Puntos Destacados">
          <ul className="space-y-2">
            {memoObj.highlights.map((h, i) => (
              <li key={i} className="flex gap-2 text-sm">
                <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-foreground" />
                {h}
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* Competitive Advantages */}
      {memoObj.competitive_advantages && (
        <Section title="Ventajas Competitivas">
          <p className="text-sm leading-relaxed text-foreground">{memoObj.competitive_advantages}</p>
        </Section>
      )}

      {/* 5. Market Fundamentals */}
      <Section title="Fundamentos de Mercado">
        <p className="text-sm leading-relaxed text-foreground">{memoObj.market_fundamentals}</p>
      </Section>

      {/* 6. Comparables */}
      {memoObj.comparables?.length > 0 && (
        <Section title="Comparables">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="py-2 text-left font-medium text-muted-foreground">Proyecto</th>
                  <th className="py-2 text-left font-medium text-muted-foreground">Ubicación</th>
                  <th className="py-2 text-right font-medium text-muted-foreground">Renta/m²</th>
                  <th className="py-2 text-right font-medium text-muted-foreground">Cap Rate</th>
                  <th className="py-2 text-right font-medium text-muted-foreground">Año</th>
                </tr>
              </thead>
              <tbody>
                {memoObj.comparables.map((c, i) => (
                  <tr key={i} className="border-b border-border last:border-0">
                    <td className="py-2 font-medium">{c.project}</td>
                    <td className="py-2 text-muted-foreground">{c.location}</td>
                    <td className="py-2 text-right">{c.rent_m2}</td>
                    <td className="py-2 text-right">{c.cap_rate}</td>
                    <td className="py-2 text-right">{c.year}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Section>
      )}

      {/* 7. Budget */}
      {memoObj.budget && (
        <Section title="Desglose de Presupuesto">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="py-2 text-left font-medium text-muted-foreground">Categoría</th>
                  <th className="py-2 text-right font-medium text-muted-foreground">Monto (MM COP)</th>
                  <th className="py-2 text-right font-medium text-muted-foreground">%</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-border">
                  <td className="py-2 font-medium">Terreno</td>
                  <td className="py-2 text-right">{memoObj.budget.land}</td>
                  <td className="py-2 text-right">{memoObj.budget.land_pct}</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-2 font-medium">Costos Duros</td>
                  <td className="py-2 text-right">{memoObj.budget.hard_costs}</td>
                  <td className="py-2 text-right">{memoObj.budget.hard_costs_pct}</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-2 font-medium">Costos Blandos</td>
                  <td className="py-2 text-right">{memoObj.budget.soft_costs}</td>
                  <td className="py-2 text-right">{memoObj.budget.soft_costs_pct}</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-2 font-medium">Contingencia</td>
                  <td className="py-2 text-right">{memoObj.budget.contingency}</td>
                  <td className="py-2 text-right">{memoObj.budget.contingency_pct}</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-2 font-medium">Costos Financieros</td>
                  <td className="py-2 text-right">{memoObj.budget.financing_costs}</td>
                  <td className="py-2 text-right">{memoObj.budget.financing_costs_pct}</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-2 font-medium">Otros</td>
                  <td className="py-2 text-right">{memoObj.budget.other}</td>
                  <td className="py-2 text-right">{memoObj.budget.other_pct}</td>
                </tr>
                <tr className="border-t-2 border-border font-semibold">
                  <td className="py-2">Total</td>
                  <td className="py-2 text-right">{memoObj.budget.total}</td>
                  <td className="py-2 text-right">100%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </Section>
      )}

      {/* Income */}
      {memoObj.income && (
        <Section title="Ingresos Proyectados">
          <InfoRow label="Ingreso Bruto Potencial" value={`${memoObj.income.gross_potential} (${memoObj.income.gross_pct})`} />
          <InfoRow label="Vacancia" value={`${memoObj.income.vacancy} (${memoObj.income.vacancy_pct})`} />
          <InfoRow label="EGI" value={`${memoObj.income.egi} (${memoObj.income.egi_pct})`} />
          <InfoRow label="OPEX" value={`${memoObj.income.opex} (${memoObj.income.opex_pct})`} />
          <InfoRow label="NOI" value={`${memoObj.income.noi} (${memoObj.income.noi_pct})`} />
        </Section>
      )}

      {/* 8. Financing */}
      {memoObj.financing && (
        <Section title="Financiamiento">
          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <h3 className="mb-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">Deuda Senior</h3>
              <InfoRow label="Monto (MM COP)" value={memoObj.financing.senior_debt_amount} />
              <InfoRow label="Términos" value={memoObj.financing.senior_debt_terms} />
            </div>
            <div>
              <h3 className="mb-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">Equity</h3>
              <InfoRow label="Monto (MM COP)" value={memoObj.financing.equity_amount} />
              <InfoRow label="Términos" value={memoObj.financing.equity_terms} />
            </div>
          </div>
        </Section>
      )}

      {/* Deal Structure */}
      {memoObj.structure && (
        <Section title="Estructura del Deal">
          <div className="grid gap-6 md:grid-cols-2">
            <div>
              <h3 className="mb-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">GP</h3>
              <InfoRow label="Capital" value={memoObj.structure.gp_capital} />
              <InfoRow label="Términos" value={memoObj.structure.gp_terms} />
            </div>
            <div>
              <h3 className="mb-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">LP</h3>
              <InfoRow label="Capital" value={memoObj.structure.lp_capital} />
              <InfoRow label="Términos" value={memoObj.structure.lp_terms} />
            </div>
          </div>
          <div className="mt-4">
            <InfoRow label="Retorno Preferente" value={memoObj.structure.preferred_return} />
            <InfoRow label="Promote/Carry" value={memoObj.structure.promote_carry} />
            <InfoRow label="Capital Calls" value={memoObj.structure.capital_calls_timeline} />
            <InfoRow label="Gobernanza" value={memoObj.structure.governance} />
          </div>
        </Section>
      )}

      {/* 9. Returns */}
      {memoObj.returns && (
        <Section title="Retornos">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-border">
                  <th className="py-2 text-left font-medium text-muted-foreground">Métrica</th>
                  <th className="py-2 text-right font-medium text-muted-foreground">Bear</th>
                  <th className="py-2 text-right font-medium text-muted-foreground">Base</th>
                  <th className="py-2 text-right font-medium text-muted-foreground">Bull</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b border-border">
                  <td className="py-2 font-medium">IRR</td>
                  <td className="py-2 text-right">{memoObj.returns.irr_bear}</td>
                  <td className="py-2 text-right">{memoObj.returns.irr_base}</td>
                  <td className="py-2 text-right">{memoObj.returns.irr_bull}</td>
                </tr>
                <tr className="border-b border-border">
                  <td className="py-2 font-medium">Equity Multiple</td>
                  <td className="py-2 text-right">{memoObj.returns.em_bear}</td>
                  <td className="py-2 text-right">{memoObj.returns.em_base}</td>
                  <td className="py-2 text-right">{memoObj.returns.em_bull}</td>
                </tr>
                <tr className="border-b border-border last:border-0">
                  <td className="py-2 font-medium">Cash-on-Cash</td>
                  <td className="py-2 text-right">{memoObj.returns.coc_bear}</td>
                  <td className="py-2 text-right">{memoObj.returns.coc_base}</td>
                  <td className="py-2 text-right">{memoObj.returns.coc_bull}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </Section>
      )}

      {/* 10. Risks */}
      {core.risks?.length > 0 && (
        <Section title="Riesgos">
          <div className="space-y-4">
            {core.risks.map((r, i) => (
              <div key={i} className="rounded-md bg-muted/50 p-4">
                <div className="mb-1 flex items-center gap-2">
                  <span className="text-sm font-medium">{r.risk_description}</span>
                  <span className="rounded-sm bg-muted px-1.5 py-0.5 text-xs text-muted-foreground">{r.severity}</span>
                </div>
                <p className="text-sm text-muted-foreground">{r.mitigation_strategy}</p>
              </div>
            ))}
          </div>
        </Section>
      )}

      {/* 11. Due Diligence */}
      {memoObj.dd && (
        <Section title="Due Diligence">
          <InfoRow label="Legal" value={memoObj.dd.legal} />
          <InfoRow label="Técnico" value={memoObj.dd.technical} />
          <InfoRow label="Ambiental" value={memoObj.dd.environmental} />
          <InfoRow label="Zonificación" value={memoObj.dd.zoning} />
          <InfoRow label="Financiero" value={memoObj.dd.financial} />
          <InfoRow label="Posesión adversa" value={memoObj.dd.adverse_possession} />
        </Section>
      )}

      {/* Rationale */}
      {memoObj.rationale?.length > 0 && (
        <Section title="Razón de Inversión">
          <ul className="space-y-2">
            {memoObj.rationale.map((r, i) => (
              <li key={i} className="flex gap-2 text-sm">
                <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-foreground" />
                {r}
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* Conditions */}
      {memoObj.conditions?.length > 0 && (
        <Section title="Condiciones">
          <ul className="space-y-2">
            {memoObj.conditions.map((c, i) => (
              <li key={i} className="flex gap-2 text-sm">
                <span className="mt-1.5 h-1.5 w-1.5 flex-shrink-0 rounded-full bg-foreground" />
                {c}
              </li>
            ))}
          </ul>
        </Section>
      )}

      {/* 12. Next Steps */}
      <Section title="Próximos Pasos">
        <p className="text-sm leading-relaxed text-foreground">{memoObj.next_steps}</p>
      </Section>
    </div>
  );
}
