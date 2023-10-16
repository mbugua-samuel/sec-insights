import { DocumentType } from "~/types/document";
import type { Document } from "~/types/document";

import type { SelectOption } from "~/types/selection";
import { filterByTickerAndType } from "./documents";

export const documentTypeOptions = [
  /* { value: DocumentType.FINANCIAL_Q1, label: DocumentType.FINANCIAL_Q1 },
  { value: DocumentType.FINANCIAL_HALF_YEAR, label: DocumentType.FINANCIAL_HALF_YEAR },
  { value: DocumentType.FINANCIAL_Q3, label: DocumentType.FINANCIAL_Q3 },
  { value: DocumentType.FINANCIAL_FULL_YEAR, label: DocumentType.FINANCIAL_FULL_YEAR }, */
  { value: DocumentType.FINANCIAL_ABRIDGED_YEAR, label: DocumentType.FINANCIAL_ABRIDGED_YEAR },
] as SelectOption[];

function documentToYearOption(document: Document): SelectOption {
  if (document.quarter) {
    return {
      value: document.id,
      label: document.year + " Q" + document.quarter,
    };
  }
  return {
    value: document.id,
    label: document.year,
  };
}

export function getAvailableYears(
  ticker: string,
  type: DocumentType,
  documents: Document[]
): SelectOption[] {
  const docs = filterByTickerAndType(ticker, type, documents);
  const yearOptions: SelectOption[] = docs.map(documentToYearOption);
  return yearOptions;
}
