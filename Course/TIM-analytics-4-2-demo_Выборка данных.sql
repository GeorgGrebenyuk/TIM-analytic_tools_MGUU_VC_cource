/*
Курс "ТИМ-ориентированная аналитика. Современные инструменты работа с данными"

Блок 4 - PostgreSQL
Официальная справка см. здесь - https://www.postgresql.org/docs/current/

Урок: Работа с таблицами - выборка данных из таблиц
Материал по теме: https://metanit.com/sql/postgresql/2.2.php

ДЕМОНСТРАЦИОННЫЙ
*/
--Выборка объектов со значением свойства в диапазоне
select * from ifc_objects_3d where net_volume > 10 and net_volume < 50 order by net_volume;

--Выборка уникальных объъектов (по атрибуту) и количество этих объектов
select DISTINCT(ifcclass), count(*) from ifc_objects_3d group by ifcclass;

--Выборка данных из двух таблиц по общему ключу

select 
	ifc_objects_3d.Name as "Объект IFC",
	ifc_objects_3d.Ifcclass as "Класс IFC",
	ifc_objects_3d.level_name as "Уровень, имя",
	ifc_storeys.global_id as "Идентификатор уровня",
	ifc_storeys.elevation as "Отметка уровня, мм"
	from ifc_objects_3d, ifc_storeys 
    where ifc_objects_3d.level_name = ifc_storeys.Name;
