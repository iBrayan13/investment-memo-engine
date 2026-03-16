import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { MemoService } from '@/services/api';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { Upload, FileJson, FileSpreadsheet, X, ArrowLeft, Loader2 } from 'lucide-react';
import { parseCSV } from '@/utils/csv';
import type { RawInput } from '@/types/memo';

export default function GenerateMemo() {
  const navigate = useNavigate();
  const [files, setFiles] = useState<File[]>([]);
  const [dragOver, setDragOver] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const handleFiles = useCallback((newFiles: FileList | File[]) => {
    const accepted = Array.from(newFiles).filter(f =>
      f.name.endsWith('.json') || f.name.endsWith('.csv')
    );
    if (accepted.length < Array.from(newFiles).length) {
      toast.error('Solo se aceptan archivos JSON y CSV');
    }
    setFiles(prev => [...prev, ...accepted]);
  }, []);

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleSubmit = async () => {
    if (files.length === 0) { toast.error('Selecciona al menos un archivo'); return; }
    setSubmitting(true);

    try {
      const rawInputs: RawInput[] = [];

      for (const file of files) {
        const text = await file.text();
        if (file.name.endsWith('.csv')) {
          const parsed = parseCSV(text);
          rawInputs.push(JSON.parse(JSON.stringify(parsed)));
        } else {
          const json = JSON.parse(text);
          // Send the entire JSON as-is (don't split arrays into individual items)
          if (Array.isArray(json)) {
            rawInputs.push(...json);
          } else {rawInputs.push(json);}
        }
      }

      const result = await MemoService.generate(rawInputs);
      toast.success('Generación iniciada');
      navigate(`/memo/${result.memo_id}`);
    } catch (err: any) {
      const msg = err?.response?.data?.detail || err?.message || 'Error al generar el memorando';
      toast.error(msg);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-surface-elevated">
      <div className="mx-auto max-w-2xl px-6 py-8">
        <Button variant="ghost" size="sm" className="mb-6 gap-2 text-muted-foreground" onClick={() => navigate('/')}>
          <ArrowLeft className="h-4 w-4" /> Volver al Dashboard
        </Button>

        <h1 className="text-2xl font-semibold text-foreground">Generar Nuevo Memorando</h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Sube archivos JSON o CSV con la información del proyecto para generar un memorando de inversión.
        </p>

        {/* Drop zone */}
        <div
          className={`mt-8 flex flex-col items-center justify-center rounded-lg border-2 border-dashed p-12 transition-colors duration-150 ${
            dragOver ? 'border-ring bg-muted/50' : 'border-border bg-card'
          }`}
          onDragOver={e => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={e => { e.preventDefault(); setDragOver(false); handleFiles(e.dataTransfer.files); }}
        >
          <Upload className="mb-3 h-8 w-8 text-muted-foreground" />
          <p className="mb-1 text-sm font-medium">Arrastra archivos aquí</p>
          <p className="mb-4 text-xs text-muted-foreground">o haz clic para seleccionar</p>
          <label>
            <input
              type="file"
              multiple
              accept=".json,.csv"
              className="hidden"
              onChange={e => e.target.files && handleFiles(e.target.files)}
            />
            <span className="cursor-pointer rounded-md bg-primary px-4 py-2 text-xs font-medium text-primary-foreground transition-colors hover:bg-primary/90">
              Seleccionar archivos
            </span>
          </label>
        </div>

        {/* File list */}
        {files.length > 0 && (
          <div className="mt-4 space-y-2">
            {files.map((f, i) => (
              <div key={i} className="flex items-center gap-3 rounded-md bg-card px-4 py-3 shadow-subtle">
                {f.name.endsWith('.csv') ? (
                  <FileSpreadsheet className="h-4 w-4 text-muted-foreground" />
                ) : (
                  <FileJson className="h-4 w-4 text-muted-foreground" />
                )}
                <span className="flex-1 truncate text-sm">{f.name}</span>
                <span className="text-xs text-muted-foreground">{(f.size / 1024).toFixed(1)} KB</span>
                <button onClick={() => removeFile(i)} className="text-muted-foreground transition-colors hover:text-destructive">
                  <X className="h-4 w-4" />
                </button>
              </div>
            ))}
          </div>
        )}

        <Button
          className="mt-6 w-full gap-2"
          onClick={handleSubmit}
          disabled={files.length === 0 || submitting}
        >
          {submitting ? <Loader2 className="h-4 w-4 animate-spin" /> : null}
          {submitting ? 'Generando...' : 'Generar Memorando'}
        </Button>
      </div>
    </div>
  );
}
