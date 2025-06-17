#!/usr/bin/env python3
import mysql.connector
import json
from datetime import datetime
import os

# Database configurations
PRODUCT_DB = {
    'host': 'localhost',
    'port': 3301,
    'user': 'root',
    'password': 'root',
    'database': 'productservicedb'
}

BASKET_DB = {
    'host': 'localhost',
    'port': 3309,
    'user': 'root',
    'password': 'root',
    'database': 'basketservicedb'
}

def get_connection(db_config):
    return mysql.connector.connect(**db_config)

def get_table_data(cursor, table_name):
    """Get all data from a table"""
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return columns, rows
    except Exception as e:
        print(f"❌ Error getting data from {table_name}: {e}")
        return None, None

def generate_insert_script(table_name, columns, rows):
    """Generate INSERT script for a table"""
    if not rows:
        return f"-- Table {table_name} is empty\n"
    
    script = f"-- INSERT statements for table {table_name}\n"
    script += f"-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for row in rows:
        values = []
        for value in row:
            if value is None:
                values.append("NULL")
            elif isinstance(value, (int, float)):
                values.append(str(value))
            elif isinstance(value, str):
                # Escape single quotes
                escaped_value = value.replace("'", "''")
                values.append(f"'{escaped_value}'")
            elif hasattr(value, 'strftime'):  # Handle datetime objects
                values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
            else:
                values.append(f"'{str(value)}'")
        
        script += f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});\n"
    
    script += "\n"
    return script

def backup_database(db_config, db_name):
    """Backup entire database"""
    print(f"🔍 {db_name} veritabanı yedekleniyor...")
    
    conn = get_connection(db_config)
    cursor = conn.cursor()
    
    try:
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        print(f"📊 {len(tables)} tablo bulundu: {', '.join(tables)}")
        
        # Create backup directory
        backup_dir = f"database_backups/{db_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup each table
        all_insert_scripts = ""
        table_stats = {}
        
        for table in tables:
            print(f"📦 {table} tablosu yedekleniyor...")
            
            columns, rows = get_table_data(cursor, table)
            if columns and rows is not None:
                # Generate INSERT script
                insert_script = generate_insert_script(table, columns, rows)
                all_insert_scripts += insert_script
                
                # Save individual table script
                with open(f"{backup_dir}/{table}_insert.sql", "w", encoding="utf-8") as f:
                    f.write(insert_script)
                
                # Save as JSON for programmatic access (convert datetime objects)
                json_rows = []
                for row in rows:
                    json_row = []
                    for value in row:
                        if hasattr(value, 'strftime'):  # Handle datetime objects
                            json_row.append(value.strftime('%Y-%m-%d %H:%M:%S'))
                        else:
                            json_row.append(value)
                    json_rows.append(json_row)
                
                table_data = {
                    "table_name": table,
                    "columns": columns,
                    "rows": json_rows,
                    "row_count": len(rows)
                }
                
                with open(f"{backup_dir}/{table}_data.json", "w", encoding="utf-8") as f:
                    json.dump(table_data, f, ensure_ascii=False, indent=2)
                
                table_stats[table] = len(rows)
                print(f"   ✅ {len(rows)} satır yedeklendi")
            else:
                print(f"   ❌ {table} tablosu yedeklenemedi")
        
        # Save complete INSERT script
        complete_script = f"""-- Complete INSERT script for {db_name}
-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- Total tables: {len(tables)}
-- Total rows: {sum(table_stats.values())}

"""
        complete_script += all_insert_scripts
        
        with open(f"{backup_dir}/complete_{db_name}_insert.sql", "w", encoding="utf-8") as f:
            f.write(complete_script)
        
        # Save database summary
        summary = {
            "database_name": db_name,
            "backup_date": datetime.now().isoformat(),
            "tables": table_stats,
            "total_tables": len(tables),
            "total_rows": sum(table_stats.values())
        }
        
        with open(f"{backup_dir}/database_summary.json", "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        
        print(f"\n✅ {db_name} yedekleme tamamlandı!")
        print(f"📁 Yedek klasörü: {backup_dir}")
        print(f"📊 Tablo istatistikleri:")
        for table, count in table_stats.items():
            print(f"   - {table}: {count} satır")
        print(f"📈 Toplam: {sum(table_stats.values())} satır")
        
        return backup_dir, summary
        
    except Exception as e:
        print(f"❌ {db_name} yedekleme hatası: {e}")
        return None, None
    finally:
        conn.close()

def main():
    """Main function to backup all databases"""
    print("🚀 Tüm veritabanları yedekleniyor...")
    print("=" * 60)
    
    # Create main backup directory
    main_backup_dir = f"database_backups/complete_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(main_backup_dir, exist_ok=True)
    
    all_summaries = {}
    
    # Backup productservicedb
    print("\n" + "=" * 60)
    product_backup_dir, product_summary = backup_database(PRODUCT_DB, "productservicedb")
    if product_summary:
        all_summaries["productservicedb"] = product_summary
    
    # Backup basketservicedb
    print("\n" + "=" * 60)
    basket_backup_dir, basket_summary = backup_database(BASKET_DB, "basketservicedb")
    if basket_summary:
        all_summaries["basketservicedb"] = basket_summary
    
    # Create master summary
    if all_summaries:
        master_summary = {
            "backup_date": datetime.now().isoformat(),
            "databases": all_summaries,
            "total_databases": len(all_summaries),
            "total_tables": sum(db["total_tables"] for db in all_summaries.values()),
            "total_rows": sum(db["total_rows"] for db in all_summaries.values())
        }
        
        with open(f"{main_backup_dir}/master_summary.json", "w", encoding="utf-8") as f:
            json.dump(master_summary, f, ensure_ascii=False, indent=2)
        
        print("\n" + "=" * 60)
        print("🎉 TÜM VERİTABANLARI YEDEKLENDİ!")
        print("=" * 60)
        print(f"📁 Ana yedek klasörü: {main_backup_dir}")
        print(f"📊 Toplam veritabanı: {len(all_summaries)}")
        print(f"📊 Toplam tablo: {master_summary['total_tables']}")
        print(f"📊 Toplam satır: {master_summary['total_rows']}")
        
        # Create a simple restore script
        restore_script = f"""-- Database Restore Script
-- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- This script will restore all databases from backup

-- Product Service Database (Port 3301)
-- Run these commands on productservicedb:

"""
        
        if product_backup_dir:
            restore_script += f"-- Source: {product_backup_dir}/complete_productservicedb_insert.sql\n"
        
        restore_script += """
-- Basket Service Database (Port 3309)  
-- Run these commands on basketservicedb:

"""
        
        if basket_backup_dir:
            restore_script += f"-- Source: {basket_backup_dir}/complete_basketservicedb_insert.sql\n"
        
        restore_script += """
-- Instructions:
-- 1. First, create the databases and tables with proper schemas
-- 2. Then run the INSERT scripts from the backup folders
-- 3. Make sure to run them in the correct order (tables with foreign keys last)
"""
        
        with open(f"{main_backup_dir}/RESTORE_INSTRUCTIONS.sql", "w", encoding="utf-8") as f:
            f.write(restore_script)
        
        print(f"\n📋 Restore talimatları: {main_backup_dir}/RESTORE_INSTRUCTIONS.sql")
        print(f"📋 Master özet: {main_backup_dir}/master_summary.json")

if __name__ == "__main__":
    main() 