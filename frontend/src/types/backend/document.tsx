export enum BackendDocumentType {
  FINANCIAL_Q1 = "Q1",
  FINANCIAL_HALF_YEAR = "HALF_YEAR",
  FINANCIAL_Q3 = "Q3",
  FINANCIAL_FULL_YEAR = "FULL_YEAR",
}

export interface BackendDocument {
  created_at: string;
  id: string;
  updated_at: string;
  metadata_map: BackendMetadataMap;
  url: string;
}

export interface BackendMetadataMap {
  ke_document: BackendSecDocument;
}

export interface BackendSecDocument {
  company_name: string;
  company_ticker: string;
  doc_type: BackendDocumentType;
  year: number;
  quarter: number;
}
