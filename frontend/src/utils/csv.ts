/**
 * Robust CSV parser that handles:
 * - Quoted fields containing commas, newlines, and double-quotes
 * - Fields with escaped quotes ("" inside quoted fields)
 * - Mixed quoted and unquoted fields
 */
export const parseCSV = (text: string): Record<string, string>[] => {
  const rows = parseCSVRows(text);
  if (rows.length < 2) return [];
  const headers = rows[0];
  return rows.slice(1).map(row => {
    return headers.reduce((obj, header, i) => {
      obj[header] = row[i] ?? '';
      return obj;
    }, {} as Record<string, string>);
  });
};

function parseCSVRows(text: string): string[][] {
  const rows: string[][] = [];
  let current = '';
  let inQuotes = false;
  let row: string[] = [];

  for (let i = 0; i < text.length; i++) {
    const ch = text[i];
    const next = text[i + 1];

    if (inQuotes) {
      if (ch === '"') {
        if (next === '"') {
          current += '"';
          i++; // skip escaped quote
        } else {
          inQuotes = false;
        }
      } else {
        current += ch;
      }
    } else {
      if (ch === '"') {
        inQuotes = true;
      } else if (ch === ',') {
        row.push(current.trim());
        current = '';
      } else if (ch === '\n' || (ch === '\r' && next === '\n')) {
        row.push(current.trim());
        if (row.some(cell => cell !== '')) {
          rows.push(row);
        }
        row = [];
        current = '';
        if (ch === '\r') i++; // skip \n after \r
      } else {
        current += ch;
      }
    }
  }

  // Last field/row
  row.push(current.trim());
  if (row.some(cell => cell !== '')) {
    rows.push(row);
  }

  return rows;
}
