import {BackendDocument} from "~/types/backend/document";
import {Document} from "~/types/document";
import {documentColors} from "~/utils/colors";

export const fromBackendDocumentToFrontend = (
  backendDocuments: BackendDocument[]
) => {
  const frontendDocs: Document[] = [];
  backendDocuments.map((backendDoc, index) => {
    const frontendDocType = backendDoc.metadata_map.ke_document.doc_type;

    // we have 10 colors for 10 documents
    const colorIndex = index < 10 ? index : 0;
    const payload = {
      id: backendDoc.id,
      url: backendDoc.url,
      ticker: backendDoc.metadata_map.ke_document.company_ticker,
      fullName: backendDoc.metadata_map.ke_document.company_name,
      year: String(backendDoc.metadata_map.ke_document.year),
      docType: frontendDocType,
      color: documentColors[colorIndex],
      quarter: backendDoc.metadata_map.ke_document.quarter || "",
    } as Document;
    frontendDocs.push(payload);
  });
  return frontendDocs;
};
