INSERT INTO valoracion VALUES(1,'10/10',5, 6, 7);
INSERT INTO valoracion VALUES(2,'maquina',4, 8, 7);
INSERT INTO valoracion VALUES(3,'mojón',1, 7, 9);

INSERT INTO deseados VALUES(7,1);
INSERT INTO deseados VALUES(7,7);

INSERT INTO categoria VALUES('Vehículos');
INSERT INTO categoria VALUES('Moda');


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
