/*
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 4 - PostgreSQL
Официальная справка см. здесь - https://www.postgresql.org/docs/current/

Урок: Работа с таблицами - данные инженерных сетей
Материал по теме: https://metanit.com/sql/postgresql/2.2.php


*/
--Поверхности
drop table if exists surfaces;
create table if not exists  surfaces 
(
	id serial primary key,
	Name CHARACTER VARYING(256),
	geom geometry(TINZ)
);
alter table surfaces alter column geom type geometry(TINZ) using ST_Force3D(geom);
copy surfaces (Name, geom) from 'E:\Temp\arch_surfaces.txt' DELIMITER '|' CSV Header;
--Сети (наименования)
drop table if exists pipe_networks;
create table if not exists pipe_networks 
(
	id serial primary key,
	Name CHARACTER VARYING(256),
	Description CHARACTER VARYING(256)
);
copy pipe_networks (Name, Description) from 'E:\Temp\arch_pipe_network.txt'
	DELIMITER '|' CSV Header;

--Колодцы
drop table if exists structs;
create table if not exists  structs 
(
	id serial primary key,
	Name CHARACTER VARYING(256),
	Description CHARACTER VARYING(256),
	Parent_network CHARACTER VARYING(256),
	geom geometry(PointZ)
);
alter table structs alter column geom type geometry(PointZ) using ST_Force3D(geom);
copy structs (Name, Description, Parent_network, geom) from 'E:\Temp\arch_structs.txt'
	DELIMITER '|' CSV Header;
--Трубы
drop table if exists pipes;
create table if not exists pipes 
(
	id serial primary key,
	Name CHARACTER VARYING(256),
	Description CHARACTER VARYING(256),
	Parent_network CHARACTER VARYING(256),
	Diameter real,
	Thickness real,
	geom geometry(LINESTRINGZ)
);
alter table pipes alter column geom type geometry(LineStringZ) using ST_Force3D(geom);
copy pipes (Name, Description, Parent_network, Diameter, Thickness, geom) from 'E:\Temp\arch_pipes.txt'
	DELIMITER '|' CSV Header;
