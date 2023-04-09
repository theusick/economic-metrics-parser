def convert_company_name(row_company_name: str) -> str:
    return row_company_name.strip().replace('«', '').replace('»', '').lower()
