CREATE TABLE IF NOT EXISTS producto (
    producto_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    denominacion VARCHAR(45),
    precio DECIMAL (6, 2)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS domicilio (
    domicilio_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    calle VARCHAR(50),
    numero VARCHAR(10),
    planta INT(3),
    puerta VARCHAR(10),
    ciudad VARCHAR(30)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS cliente (
    cliente_id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    denominacion VARCHAR(45),
    nif VARCHAR(15),
    domicilio INT(11),
    FOREIGN KEY(domicilio) REFERENCES domicilio(domicilio_id) ON DELETE SET NULL
) ENGINE=InnoDB;

