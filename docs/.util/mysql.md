# MySQL / MariaDB Command Reference

## DDL (Data Definition Language)
DDL commands define and modify database structure: databases, tables, indexes, and constraints.
- `CREATE DATABASE db_name;` - create a new database
- `DROP DATABASE db_name;` - delete a database
- `USE db_name;` - switch current database
- `CREATE TABLE table_name (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  );` - create a new table
- `DROP TABLE table_name;` - delete a table
- `TRUNCATE TABLE table_name;` - remove all rows and reset auto-increment
- `ALTER TABLE table_name ADD COLUMN column_name VARCHAR(255);` - add a new column
- `ALTER TABLE table_name DROP COLUMN column_name;` - drop a column
- `ALTER TABLE table_name MODIFY COLUMN column_name TEXT;` - change column type
- `ALTER TABLE table_name CHANGE COLUMN old_name new_name INT;` - rename and change type
- `ALTER TABLE table_name RENAME TO new_table_name;` - rename table
- `ALTER TABLE table_name ADD PRIMARY KEY (id);` - add primary key constraint
- `ALTER TABLE table_name DROP PRIMARY KEY;` - remove primary key
- `ALTER TABLE table_name ADD INDEX idx_name (column_name);` - add index
- `ALTER TABLE table_name DROP INDEX idx_name;` - remove index
- `ALTER TABLE table_name ADD UNIQUE (column_name);` - add unique constraint
- `ALTER TABLE table_name ADD FOREIGN KEY (fk_column) REFERENCES other_table(id);` - add foreign key

## DML (Data Manipulation Language)
DML commands insert, update and delete rows in existing tables.
- `INSERT INTO table_name (col1, col2) VALUES ('value1', 'value2');` - insert a new row
- `INSERT INTO table_name SET col1='value1', col2='value2';` - alternative insert syntax
- `INSERT INTO table_name (col1, col2)
    SELECT col1, col2 FROM other_table;` - insert from query results
- `INSERT IGNORE INTO table_name (col1, col2) VALUES ('value1', 'value2');` - ignore duplicate-key errors
- `INSERT INTO table_name (col1, col2) VALUES ('value1', 'value2')
    ON DUPLICATE KEY UPDATE col2 = VALUES(col2);` - upsert behavior
- `UPDATE table_name SET col1='value' WHERE id=1;` - update rows matching condition
- `UPDATE table_name SET col1='value' WHERE condition;` - update multiple rows
- `DELETE FROM table_name WHERE id=1;` - delete specific row
- `DELETE FROM table_name WHERE condition;` - delete rows matching condition
- `DELETE FROM table_name;` - delete all rows

## DQL (Data Query Language)
DQL commands retrieve and filter data using SELECT.
- `SELECT * FROM table_name;` - fetch all columns
- `SELECT col1, col2 FROM table_name WHERE condition ORDER BY col1 DESC LIMIT 10;` - filtered query with sorting and pagination
- `SELECT DISTINCT col FROM table_name;` - remove duplicate values
- `SELECT COUNT(*) FROM table_name;` - count rows
- `SELECT col1, SUM(col2) FROM table_name GROUP BY col1;` - aggregation by group
- `SELECT col1, COUNT(*) FROM table_name HAVING COUNT(*) > 1;` - filter groups
- `SELECT a.*, b.* FROM table_a a
    JOIN table_b b ON a.id = b.a_id;` - inner join
- `SELECT a.*, b.* FROM table_a a
    LEFT JOIN table_b b ON a.id = b.a_id;` - left join
- `SELECT a.*, b.* FROM table_a a
    RIGHT JOIN table_b b ON a.id = b.a_id;` - right join
- `SELECT a.*, b.* FROM table_a a
    CROSS JOIN table_b b;` - cross join
- `SELECT a.*, b.* FROM table_a a
    JOIN table_b b ON a.id = b.a_id
    JOIN table_c c ON b.c_id = c.id;` - multiple joins
- `SELECT * FROM table_name WHERE col IN (SELECT col FROM other_table);` - subquery

## DCL (Data Control Language)
DCL commands manage permissions and user accounts.
- `CREATE USER 'user'@'host' IDENTIFIED BY 'password';` - create database user
- `DROP USER 'user'@'host';` - delete database user
- `GRANT SELECT, INSERT ON db_name.* TO 'user'@'host';` - grant permissions
- `REVOKE INSERT ON db_name.* FROM 'user'@'host';` - revoke permissions
- `SHOW GRANTS FOR 'user'@'host';` - view grants for user
- `SHOW GRANTS FOR CURRENT_USER();` - view current user grants
- `ALTER USER 'user'@'host' IDENTIFIED BY 'new_password';` - change user password
- `SET PASSWORD FOR 'user'@'host' = 'new_password';` - set password (MySQL syntax may vary)

## TCL (Transaction Control Language)
TCL commands control transaction boundaries and rollback points.
- `START TRANSACTION;` - begin a transaction
- `BEGIN;` - alias for starting transaction
- `COMMIT;` - commit current transaction
- `ROLLBACK;` - rollback current transaction
- `SAVEPOINT savepoint_name;` - create a savepoint
- `ROLLBACK TO SAVEPOINT savepoint_name;` - rollback to a savepoint
- `RELEASE SAVEPOINT savepoint_name;` - remove savepoint

## Views
Views are stored queries treated like virtual tables.
- `CREATE VIEW view_name AS
    SELECT col1, col2 FROM table_name WHERE condition;` - create view
- `CREATE OR REPLACE VIEW view_name AS
    SELECT col1, col2 FROM table_name;` - update view definition
- `DROP VIEW view_name;` - delete view
- `DROP VIEW IF EXISTS view_name;` - delete view if exists
- `SELECT * FROM view_name;` - query view
- `SHOW FULL TABLES WHERE Table_type = 'VIEW';` - list views
- `SHOW CREATE VIEW view_name;` - show view SQL

## Stored Procedures and Functions
Stored routines encapsulate reusable logic.
- `DELIMITER $$`
- `CREATE PROCEDURE proc_name(IN param1 INT, OUT param2 VARCHAR(255))
  BEGIN
    SELECT name INTO param2 FROM table_name WHERE id = param1;
  END $$` - create procedure with IN/OUT parameters
- `CREATE PROCEDURE proc_name()
  BEGIN
    INSERT INTO table_name (col1) VALUES ('value');
  END $$` - create procedure without parameters
- `CREATE FUNCTION func_name(val INT) RETURNS INT
  DETERMINISTIC
  RETURN val * 2; $$` - create scalar function
- `CALL proc_name(1, @output);` - execute procedure
- `SELECT @output;` - read output variable
- `DROP PROCEDURE proc_name;` - remove procedure
- `DROP FUNCTION func_name;` - remove function
- `SHOW PROCEDURE STATUS WHERE Db = 'db_name';` - list procedures
- `SHOW FUNCTION STATUS WHERE Db = 'db_name';` - list functions
- `SHOW CREATE PROCEDURE proc_name;` - show procedure SQL
- `SHOW CREATE FUNCTION func_name;` - show function SQL
- `DELIMITER ;`

## Triggers
Triggers execute automatically on table events.
- `DELIMITER $$`
- `CREATE TRIGGER trigger_name
    BEFORE INSERT ON table_name
    FOR EACH ROW
  BEGIN
    SET NEW.created_at = NOW();
  END $$` - before insert trigger
- `CREATE TRIGGER trigger_name
    AFTER UPDATE ON table_name
    FOR EACH ROW
  BEGIN
    INSERT INTO audit_table (table_id, changed_at)
    VALUES (NEW.id, NOW());
  END $$` - after update trigger
- `DROP TRIGGER trigger_name;` - delete trigger
- `DROP TRIGGER IF EXISTS trigger_name;` - delete if exists
- `SHOW TRIGGERS;` - list triggers
- `SHOW CREATE TRIGGER trigger_name;` - show trigger SQL
- `DELIMITER ;`

## SHOW and Information Commands
Useful inspection commands for MySQL/MariaDB metadata and runtime state.
- `SHOW DATABASES;` - list databases
- `SHOW TABLES;` - list tables in current database
- `SHOW TABLES FROM db_name;` - list tables in specified database
- `SHOW COLUMNS FROM table_name;` - describe table columns
- `SHOW FULL COLUMNS FROM table_name;` - detailed column info
- `SHOW INDEX FROM table_name;` - list indexes
- `SHOW CREATE TABLE table_name;` - table creation DDL
- `SHOW CREATE DATABASE db_name;` - database creation DDL
- `SHOW STATUS;` - server status variables
- `SHOW VARIABLES;` - server configuration variables
- `SHOW VARIABLES LIKE 'version%';` - version-related variables
- `SHOW PROCESSLIST;` - active connections and queries
- `SHOW ENGINE INNODB STATUS;` - InnoDB engine status
- `SHOW WARNINGS;` - recent warnings
- `SHOW ERRORS;` - recent errors

## MariaDB-specific / Useful Commands
- `SELECT VERSION();` - server version
- `SELECT @@version_comment;` - distribution comment
- `SELECT @@sql_mode;` - current SQL mode
- `SET sql_mode = 'STRICT_ALL_TABLES';` - change SQL mode
- `SHOW PLUGINS;` - list installed plugins
- `SHOW CREATE EVENT event_name;` - show event SQL
- `SHOW EVENTS;` - list scheduled events
- `SHOW CREATE PROCEDURE proc_name;` - show procedure SQL
- `SHOW CREATE VIEW view_name;` - show view SQL

## Backup and Restore
- `mysqldump -u user -p db_name > backup.sql` - export database
- `mysqldump -u user -p --tables db_name table_name > table_backup.sql` - export single table
- `mysql -u user -p db_name < backup.sql` - import backup
