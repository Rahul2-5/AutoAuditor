from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse, StreamingResponse
import pandas as pd
import numpy as np
import io
from datetime import datetime
import json

from services.data_prep_agent import orchestrator
from services.auditor import auditor
from services.full_audit_pipeline import pipeline

router = APIRouter()


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy/pandas types"""
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64)):
            return int(obj)
        if isinstance(obj, (np.floating, np.float64)):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        if pd.isna(obj):
            return None
        if isinstance(obj, (pd.Timestamp, np.datetime64)):
            return str(obj.date() if hasattr(obj, 'date') else obj)
        return super().default(obj)


@router.post("/prepare")
async def prepare_expense_data(file: UploadFile = File(...)):
    """
    MAIN ENDPOINT: Prepare expense data for AI analysis
    
    Dynamic column mapping + cleaning + feature enrichment
    """
    try:
        # Read CSV
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Run preparation pipeline
        result = orchestrator.prepare(df)
        
        if result['status'] != 'success':
            error_response = {
                'status': 'error',
                'errors': result['errors'],
                'execution_log': result['execution_log']
            }
            return JSONResponse(
                status_code=400,
                content=json.loads(json.dumps(error_response, cls=NumpyEncoder))
            )
        
        # Extract cleaned dataframe
        df_prepared = result['data']
        
        # Prepare preview records
        preview_records = []
        for _, row in df_prepared.head(5).iterrows():
            record = {}
            for col in df_prepared.columns:
                val = row[col]
                if pd.isna(val):
                    record[col] = None
                elif isinstance(val, (pd.Timestamp, np.datetime64)):
                    record[col] = str(val.date() if hasattr(val, 'date') else val)
                elif isinstance(val, (np.integer, np.int64)):
                    record[col] = int(val)
                elif isinstance(val, (np.floating, np.float64)):
                    record[col] = float(val)
                elif isinstance(val, (np.bool_,)):
                    record[col] = bool(val)
                else:
                    record[col] = str(val)
            preview_records.append(record)
        
        # Build response
        response_data = {
            'status': 'success',
            'message': 'Data prepared successfully',
            'summary': result['summary'],
            'flags': result['flags'],
            'data_preview': {
                'total_rows': int(len(df_prepared)),
                'columns': list(df_prepared.columns),
                'first_5_records': preview_records
            },
            'execution_log': result['execution_log']
        }
        
        # Serialize with NumpyEncoder to handle all numpy types
        serialized = json.loads(json.dumps(response_data, cls=NumpyEncoder))
        
        return JSONResponse(
            status_code=200,
            content=serialized
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                'status': 'error',
                'message': 'File processing failed',
                'details': str(e)
            }
        )


@router.post("/export-prepared-data")
async def export_prepared_data(file: UploadFile = File(...)):
    """Export prepared data as CSV file"""
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        result = orchestrator.prepare(df)
        
        if result['status'] != 'success':
            error_response = {
                'status': 'error',
                'errors': result['errors']
            }
            return JSONResponse(
                status_code=400,
                content=json.loads(json.dumps(error_response, cls=NumpyEncoder))
            )
        
        df_prepared = result['data']
        
        # Convert to CSV
        csv_buffer = io.BytesIO()
        df_prepared.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)
        
        return StreamingResponse(
            iter([csv_buffer.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": 
                f"attachment; filename=prepared_expenses_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={'status': 'error', 'details': str(e)}
        )


@router.post("/analyze")
async def analyze_expenses(audit_data: dict):
    """
    ADVANCED AUDITOR ENDPOINT: Analyze expense data for audit intelligence
    
    Accepts structured JSON with:
    - summary_statistics
    - enriched_features
    - policy_violations
    - flagged_transactions
    - transactions
    
    Returns comprehensive audit report with:
    - risk assessment
    - violation analysis
    - anomaly detection
    - fraud signals
    - financial insights
    - recommendations
    - cost optimization tips
    - visualization data
    """
    try:
        # Run comprehensive audit analysis
        audit_report = auditor.analyze(audit_data)
        
        # Ensure clean JSON output
        serialized_report = json.loads(
            json.dumps(audit_report, cls=NumpyEncoder)
        )
        
        return JSONResponse(
            status_code=200,
            content=serialized_report
        )
    
    except Exception as e:
        error_response = {
            'status': 'error',
            'message': 'Audit analysis failed',
            'error_details': str(e)
        }
        return JSONResponse(
            status_code=400,
            content=error_response
        )


@router.post("/full-audit")
async def full_audit_workflow(file: UploadFile = File(...)):
    """
    COMPLETE AUTOMATED AUDIT WORKFLOW
    
    Single endpoint that:
    1. Accepts CSV file upload
    2. Prepares & cleans data
    3. Extracts features & violations
    4. Runs comprehensive audit analysis
    5. Generates complete report with summary
    
    Returns:
    - Data preparation results
    - Complete audit analysis
    - Executive summary
    - Visualization data
    - All in one JSON response
    """
    try:
        # Read uploaded file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Process through complete pipeline
        result = pipeline.process_file(df)
        
        # Serialize response
        serialized = json.loads(
            json.dumps(result, cls=NumpyEncoder)
        )
        
        status_code = 200 if result['status'] == 'success' else 400
        
        return JSONResponse(
            status_code=status_code,
            content=serialized
        )
    
    except Exception as e:
        error_response = {
            'status': 'error',
            'message': 'Full audit workflow failed',
            'error_details': str(e),
            'error_type': type(e).__name__
        }
        return JSONResponse(
            status_code=400,
            content=error_response
        )