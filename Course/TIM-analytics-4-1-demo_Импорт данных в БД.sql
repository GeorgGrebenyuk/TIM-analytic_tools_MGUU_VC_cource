/*
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 4 - PostgreSQL
Официальная справка см. здесь - https://www.postgresql.org/docs/current/

Урок: Работа с таблицами - создание и вставка из CSV файлов
Материал по теме: https://metanit.com/sql/postgresql/2.2.php

ДЕМОНСТРАЦИОННЫЙ
*/
--Создание таблиц
drop table if exists ifc_objects_3d;
create table if not exists ifc_objects_3d 
(
	id serial primary key,
	Name CHARACTER VARYING(256),
	IfcClass CHARACTER VARYING(128),
	Level_name CHARACTER VARYING(128),
	net_volume real,
	count integer,
	global_id CHARACTER VARYING(22)	
);

drop table if exists ifc_storeys;
create table if not exists ifc_storeys 
(
	id serial primary key,
	Name CHARACTER VARYING(256),
	global_id CHARACTER VARYING(22),
	Elevation real
);
--Вставка значений из текстовыйх файлов
copy ifc_objects_3d (Name,IfcClass,Level_name, net_volume,  count, global_id) from 'E:\Temp\objects_3d.txt'
	DELIMITER '|' CSV Header;
copy ifc_storeys (Name, global_id, elevation ) from 'E:\Temp\storeys.txt'
	DELIMITER '|' CSV Header;
