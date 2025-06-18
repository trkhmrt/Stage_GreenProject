-- Database Restore Script
-- Generated on 2025-06-18 02:57:28
-- This script will restore all databases from backup

-- Product Service Database (Port 3301)
-- Run these commands on productservicedb:

-- Source: database_backups/productservicedb_20250618_025728/complete_productservicedb_insert.sql

-- Basket Service Database (Port 3309)  
-- Run these commands on basketservicedb:

-- Source: database_backups/basketservicedb_20250618_025728/complete_basketservicedb_insert.sql

-- Instructions:
-- 1. First, create the databases and tables with proper schemas
-- 2. Then run the INSERT scripts from the backup folders
-- 3. Make sure to run them in the correct order (tables with foreign keys last)
