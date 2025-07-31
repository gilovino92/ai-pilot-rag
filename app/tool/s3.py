import boto3
from app.core.config import settings
from io import BytesIO
from PyPDF2 import PdfReader
import asyncio
from app.utils.helpers import split_content_into_chunks
from app.tool.vectorDB_tool import store_vector_record_with_tenant_id
from app.tool.tenant import update_document_status

def get_s3_client():
    """Return the S3 client instance."""
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )
    return s3_client

def get_s3_bucket():
    """Return the S3 bucket instance."""
    s3_client = get_s3_client()
    bucket = s3_client.Bucket(settings.AWS_S3_BUCKET)
    return bucket

async def process_s3_object(tenant_id: str, key: str):
    """Return the S3 object instance."""
    s3_client = get_s3_client()
    try:
        # Get the PDF object from S3
        response = s3_client.get_object(Bucket=settings.AWS_S3_BUCKET, Key=key)

        # Read the PDF content into memory
        pdf_data = response['Body'].read()
        
        # Create BytesIO object from PDF data
        pdf_file = BytesIO(pdf_data)
        reader = PdfReader(pdf_file)
        content = " ".join([page.extract_text() for page in reader.pages])
        chunks = split_content_into_chunks(content,key);
        await store_vector_record_with_tenant_id(chunks, tenant_id);
        await update_document_status(key, 'done');
        print(f'\033[43m\033[30mSuccessfully processed S3 object {key} of tenant {tenant_id}\033[0m')

    except Exception as e:
        print(f"Error: {str(e)}")


