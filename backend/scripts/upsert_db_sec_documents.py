import asyncio
from pathlib import Path

from fastapi.encoders import jsonable_encoder
from fire import Fire
from pytickersymbols import PyTickerSymbols
from tqdm import tqdm

from app.api import crud
from app.db.session import SessionLocal
from app.models.db import Document
from app.schema import (
    DocumentMetadata,
    DocumentMetadataMap,
    DocumentMetadataKeysEnum,
    Document, DocumentTypeEnum,
)
from file_utils import get_available_filings, Filing
from stock_utils import get_stocks_by_symbol, Stock

DEFAULT_URL_BASE = "https://dl94gqvzlh4k8.cloudfront.net"
DEFAULT_DOC_DIR = "data/"


async def upsert_document(doc_dir: str, stock: Stock, filing: Filing, url_base: str):
    # construct a string for just the document's sub-path after the doc_dir
    # e.g. "sec-edgar-filings/AAPL/10-K/0000320193-20-000096/filing-details.pdf"
    doc_path = Path(filing.file_path).relative_to(doc_dir)
    url_path = url_base.rstrip("/") + "/" + str(doc_path).lstrip("/")
    doc_type = (
        DocumentTypeEnum.FINANCIAL_Q1
        if filing.filing_type == "Q1"
        else DocumentTypeEnum.FINANCIAL_HALF_YEAR
        if filing.filing_type == "HALF_YEAR"
        else DocumentTypeEnum.FINANCIAL_Q3
        if filing.filing_type == "Q3"
        else DocumentTypeEnum.FINANCIAL_FULL_YEAR
    )
    sec_doc_metadata = DocumentMetadata(
        company_name=stock.name,
        company_ticker=stock.symbol,
        doc_type=doc_type,
        year=filing.year,
        quarter=filing.quarter,
        accession_number=filing.accession_number,
        cik=filing.cik,
        period_of_report_date=filing.period_of_report_date,
        filed_as_of_date=filing.filed_as_of_date,
        date_as_of_change=filing.date_as_of_change,
    )
    metadata_map: DocumentMetadataMap = {
        DocumentMetadataKeysEnum.KE_DOCUMENT: jsonable_encoder(
            sec_doc_metadata.dict(exclude_none=True)
        )
    }
    doc = Document(url=str(url_path), metadata_map=metadata_map)
    async with SessionLocal() as db:
        await crud.upsert_document_by_url(db, doc)


async def async_upsert_documents_from_filings(url_base: str, doc_dir: str):
    """
    Upserts SEC documents into the database based on what has been downloaded to the filesystem.
    """
    filings = get_available_filings(doc_dir)
    stocks_data = PyTickerSymbols()
    stocks_dict = get_stocks_by_symbol(stocks_data.get_all_indices())
    for filing in tqdm(filings, desc="Upserting docs from filings"):
        if filing.symbol not in stocks_dict:
            print(f"Symbol {filing.symbol} not found in stocks_dict. Skipping.")
            continue
        stock = stocks_dict[filing.symbol]
        await upsert_document(doc_dir, stock, filing, url_base)


def main_upsert_documents_from_filings(
    url_base: str = DEFAULT_URL_BASE, doc_dir: str = DEFAULT_DOC_DIR
):
    """
    Upserts SEC documents into the database based on what has been downloaded to the filesystem.
    """

    asyncio.run(async_upsert_documents_from_filings(url_base, doc_dir))


if __name__ == "__main__":
    Fire(main_upsert_documents_from_filings)
