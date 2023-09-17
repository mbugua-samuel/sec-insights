import { DocumentColorEnum } from "~/utils/colors";
import {BackendDocumentType} from "~/types/backend/document";

export enum DocumentType {
  FINANCIAL_Q1 = "Q1",
  FINANCIAL_HALF_YEAR = "HALF_YEAR",
  FINANCIAL_Q3 = "Q3",
  FINANCIAL_FULL_YEAR = "FULL_YEAR",
}

export type Ticker = {
  ticker: string;
  fullName: string;
};

export interface Document extends Ticker {
  id: string;
  url: string;
  year: string;
  docType: BackendDocumentType;
  quarter?: string;
  color: DocumentColorEnum;
}
