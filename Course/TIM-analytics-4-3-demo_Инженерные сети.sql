/*
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 4 - PostgreSQL
Официальная справка см. здесь - https://www.postgresql.org/docs/current/

Урок: Работа с таблицами - данные инженерных сетей
Материал по теме: https://metanit.com/sql/postgresql/2.2.php

ДЕМОНСТРАЦИОННЫЙ
*/
-- Поверхности
drop table if exists surfaces;
create table surfaces (
	id serial primary key,
	Name CHARACTER VARYING (256),
	geom geometry(TINZ)
	);
alter table surfaces alter column geom type geometry(TINZ) using st_force3d(geom);
copy surfaces (Name, geom) from 'E:\Temp\ark_surfaces.txt' DELIMITER '|' Header CSV;
--Определения сетей (наименования)
drop table if exists pipe_networks;
create table pipe_networks (
	id serial primary key,
	Name CHARACTER VARYING (256),
	Description CHARACTER VARYING (256)
	);
copy pipe_networks (Name, Description) from 'E:\Temp\ark_pipe_networks.txt' DELIMITER '|' Header CSV;

-- Колодцы
drop table if exists structs;
create table structs (
	id serial primary key,
	Name CHARACTER VARYING (256),
	Description CHARACTER VARYING (256),
	Parent_network CHARACTER VARYING (256),
	geom geometry(PointZ)
	);
alter table structs alter column geom type geometry(PointZ) using st_force3d(geom);
copy structs (Name,Description ,Parent_network, geom) from 'E:\Temp\ark_structs.txt' DELIMITER '|' Header CSV;
-- Трубы
drop table if exists pipes;
create table pipes (
	id serial primary key,
	Name CHARACTER VARYING (256),
	Description CHARACTER VARYING (256),
	Parent_network CHARACTER VARYING (256),
	Diameter real,
	Thickness real,
	geom geometry(LineStringZ)
	);
alter table pipes alter column geom type geometry(LineStringZ) using st_force3d(geom);
copy pipes (Name,Description ,Parent_network,Diameter,Thickness, geom) from 'E:\Temp\ark_pipes.txt' DELIMITER '|' Header CSV;
