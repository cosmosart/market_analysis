"""Initialize database schema."""
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.database.connection import db
import config

def main():
    """Initialize the database schema."""
    print("Initializing database schema...")
    
    # Test connection first
    if not db.test_connection():
        print("Failed to connect to database. Please check your configuration.")
        return
    
    # Initialize schema
    schema_file = config.SQL_DIR / "schema.sql"
    
    if not schema_file.exists():
        print(f"Schema file not found: {schema_file}")
        return
    
    try:
        db.initialize_schema(str(schema_file))
        print("✓ Database schema initialized successfully!")
    except Exception as e:
        print(f"✗ Failed to initialize schema: {e}")


if __name__ == "__main__":
    main()
