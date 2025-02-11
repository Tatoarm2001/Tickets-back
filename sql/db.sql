CREATE DATABASE ticket_store;
USE ticket_store;

CREATE TABLE concerts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    eventName VARCHAR(255) NOT NULL,
    img VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    dateTime DATETIME NOT NULL,
    place VARCHAR(255) NOT NULL,
    price DECIMAL(5,2) NOT NULL
)auto_increment = 1;

INSERT INTO concerts (eventName, img, description, dateTime, place, price) VALUES
('Rock Fest', 'https://example.com/rockfest.jpg', 'Festival de rock en vivo.', '2025-06-15 19:00:00', 'Estadio Nacional', 50.00),
('Jazz Night', 'https://example.com/jazznight.jpg', 'Noche de jazz con artistas internacionales.', '2025-07-20 20:30:00', 'Teatro de la Ciudad', 35.50),
('EDM Party', 'https://example.com/edmparty.jpg', 'La mejor música electrónica de la temporada.', '2025-08-05 22:00:00', 'Club Nocturno Eclipse', 45.00),
('Pop Stars Live', 'https://example.com/popstars.jpg', 'Las estrellas del pop en un concierto único.', '2025-09-10 18:00:00', 'Arena Central', 60.00),
('Indie Vibes', 'https://example.com/indievibes.jpg', 'Concierto de bandas indie emergentes.', '2025-10-12 19:30:00', 'Centro Cultural Independiente', 25.00);

select * from concerts;
delete from concerts;