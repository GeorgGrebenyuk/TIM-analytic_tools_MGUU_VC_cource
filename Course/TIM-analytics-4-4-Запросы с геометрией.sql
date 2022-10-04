--after
alter table pipes add column is_under_surface BOOLEAN;

update pipes set is_under_surface = st_intersects(surfaces.geom, geom);
SELECT * FROM public.pipes
ORDER BY id ASC LIMIT 100;