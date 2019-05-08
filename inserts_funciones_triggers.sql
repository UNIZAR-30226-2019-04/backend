INSERT INTO categoria VALUES('Coches');
INSERT INTO categoria VALUES('Inmuebles');
INSERT INTO categoria VALUES('Motos');
INSERT INTO categoria VALUES('Móviles y accesorios');
INSERT INTO categoria VALUES('TV, audio, cámaras');
INSERT INTO categoria VALUES('Ordenadores');
INSERT INTO categoria VALUES('Deportes');
INSERT INTO categoria VALUES('Bicicletas');
INSERT INTO categoria VALUES('Juegos y Consolas');
INSERT INTO categoria VALUES('Moda y accesorios');
INSERT INTO categoria VALUES('Libros y música');
INSERT INTO categoria VALUES('Servicios');
INSERT INTO categoria VALUES('Otros');

CREATE OR REPLACE FUNCTION calcular_distancia(lat1 FLOAT, lon1 FLOAT, rad1 FLOAT, lat2 FLOAT, lon2 FLOAT, rad2 FLOAT) RETURNS FLOAT AS $calcular_distancia$
  DECLARE
  BEGIN
	RETURN ACOS(SIN(PI()*lat1/180.0)*SIN(PI()*lat2/180.0)+COS(PI()*lat1/180.0)*COS(PI()*lat2/180.0)*COS(PI()*lon2/180.0-PI()*lon1/180.0))*6371000 - rad1 - rad2;
  END;
$calcular_distancia$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION actualizar_valoracion_media() RETURNS TRIGGER AS $actualizar_valoracion_media$
  DECLARE
  BEGIN
	UPDATE usuario set valoracion_media=(SELECT AVG(puntuacion) FROM valoracion WHERE puntuado=new.puntuado) WHERE id=new.puntuado;
  RETURN NEW;
  END;
$actualizar_valoracion_media$ LANGUAGE plpgsql;


CREATE TRIGGER valoracion_media AFTER INSERT
    ON valoracion FOR EACH ROW
    EXECUTE PROCEDURE actualizar_valoracion_media();
