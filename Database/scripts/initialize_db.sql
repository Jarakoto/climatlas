/* Database initialization script */
DROP DATABASE IF EXISTS climatlas;
CREATE DATABASE climatlas;
\c climatlas;

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;
COMMENT ON EXTENSION postgis IS 'PostGIS geometry, geography, and raster spatial types and functions';
SET default_with_oids = false;

/*    Create the grids schema   */
CREATE SCHEMA grids;

CREATE FUNCTION grids.fn_create_grid_table(table_name varchar)
    RETURNS VOID
    LANGUAGE plpgsql AS
$func$
BEGIN
    EXECUTE format(
        '
        CREATE TABLE IF NOT EXISTS grids.preserved_cells_%I
            (
                row INT NOT NULL,
                col INT NOT NULL,
                geom public.geometry(Geometry, 4326)
            );
        CREATE INDEX idx_preserved_cells_%I ON grids.preserved_cells_%I (row, col);
        CREATE TABLE IF NOT EXISTS grids.cut_cells_%I
            (
                row INT NOT NULL,
                col INT NOT NULL,
                geom public.geometry(Geometry, 4326)
            );
        CREATE INDEX idx_cut_cells_%I ON grids.cut_cells_%I (row, col);
        ',
        table_name,
        table_name,
        table_name,
        table_name,
        table_name,
        table_name
    );
END
$func$;

SELECT grids.fn_create_grid_table('zoom_1');
SELECT grids.fn_create_grid_table('zoom_2');
SELECT grids.fn_create_grid_table('zoom_3');
SELECT grids.fn_create_grid_table('zoom_4');

CREATE SCHEMA temperatures;
