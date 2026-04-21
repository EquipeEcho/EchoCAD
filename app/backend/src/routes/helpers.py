from fastapi import HTTPException


def safe_create(func, db, obj, msg):
    """Helper function to safely create database records with error handling."""
    try:
        return func(db, obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{msg}: {str(e)}")