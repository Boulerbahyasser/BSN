-- Insert into Category (10 categories)
INSERT INTO "category" (nom) VALUES
('Fiction'),
('Science'),
('Technology'),
('History'),
('Mystery'),
('Romance'),
('Fantasy'),
('Biography'),
('Horror'),
('Non-fiction');


-- Insert into Utilisateur (10 users with all required fields for Django User model)
INSERT INTO "Utilisateur"
(username, first_name, last_name, email, description, image, telephone, adresse, password, is_active, is_staff, is_superuser, last_login, date_joined, "isLinkedToBank")
VALUES
('user1', 'John', 'Doe', 'user1@gamil.com', 'A regular user', null, '0123456789', '123 Main St', 'pbkdf2_sha256$870000$AYGQ3BdJbGNQ8Ktp6Cwb7L$lMFZeZlOR5eFbNQPhItAsCK241lMUHWclVjbfzJdyOM=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false),
('user2', 'Jane', 'Doe', 'user2@gamil.com', 'Another regular user', null, '0123456790', '456 Side St', 'pbkdf2_sha256$870000$oJpl0GmjsPRx8hzCUf6izj$NuwXehzL+ihEa1H3mJbWdWar8zIrdqUDnQiYrATOHBM=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false),
('user3', 'Jim', 'Beam', 'user3@gamil.com', 'Lover of books', null, '0123456791', '789 High St', 'pbkdf2_sha256$870000$1lZK93SqFYeJkYoE1t9bcQ$gLqK/XZJpvwsIkmAQNzczkMOUBK3QvaGWn3faiiPAhM=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false),
('user4', 'Jack', 'Daniels', 'user4@gamil.com', 'Book enthusiast', null, '0123456792', '321 Low St', 'pbkdf2_sha256$870000$LB5POzaDP0gkUEJuZXKwfx$sTl5FOJ4T9DAewr2iArEPdr4jdacj6GwPn/GX/pxnFM=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false),
('user5', 'Jill', 'Smith', 'user5@gamil.com', 'Reader and reviewer', null, '0123456793', '654 Down St', 'pbkdf2_sha256$870000$Y01IrTO8MFRyHvApoPs3aC$4bEuQR9cuCMm78tVAH5oV4mGLQEiDsWXmROKajYq0Ho=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false),
('user6', 'Lucy', 'Green', 'user6@gamil.com', 'Book lover', null, '0123456794', '987 New St', 'pbkdf2_sha256$870000$cMFyo7e08eLTafwvils9MP$18a/AOBzlKFoeBKJStp9Bs3XjXZmNlwxeDvU+L/6HVQ=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false),
('user7', 'Maggie', 'White', 'user7@gamil.com', 'Frequent reader', null, '0123456795', '101 Oak St', 'pbkdf2_sha256$870000$V3TzLfgdwsOEn3DulZ9JrO$7PnzR+QJ/RwnNiUH/DFBk2mS1FlWUYs+JWnpPNszxwg=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false),
('user8', 'Tom', 'Blue', 'user8@gamil.com', 'Avid bookworm', null, '0123456796', '202 Pine St', 'pbkdf2_sha256$870000$meI6PbKEBPp3H5yb8wv7XD$Ok1P6PObFDG/i6BNOiqLzJRDGLLI5tjZvl5xR73AKNk=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false),
('user9', 'Eve', 'Black', 'user9@gamil.com', 'Literature fan', null, '0123456797', '303 Maple St', 'pbkdf2_sha256$870000$JErIorlcb3r8ytlV4XnRpd$oT+OfGSTrUCDrISHGRzvmo794LhFS6l3fHSlIAHptz0=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false),
('user10', 'Oscar', 'Red', 'user10@gamil.com', 'Book reviewer', null, '0123456798', '404 Birch St', 'pbkdf2_sha256$870000$s4Hp63PZzZq1BXu3A3WKxJ$eZl0vyPbRtzQookczoM3q3l8FD0ZnSBwgN0NfZeJgrs=', true, false, false, '2024-12-07 00:00:00', '2024-12-07 00:00:00', false);

-- Insert into Livre (10 general books)
INSERT INTO "livre" (titre, couverture_path, auteur, est_disponible, utilisateur_id) VALUES
('Book 1', null, 'Author 1', true, 1),
('Book 2', null, 'Author 2', true, 1),
('Book 3', null, 'Author 3', true, 1),
('Book 4', null, 'Author 4', true, 1),
('Book 5', null, 'Author 5', true, 1),
('Book 6', null, 'Author 6', true, 1),
('Book 7', null, 'Author 7', true, 1),
('Book 8', null, 'Author 8', true, 1),
('Book 9', null, 'Author 9', true, 1),
('Book 10', null, 'Author 10', true, 1);


INSERT INTO "livrePhysique" (livre_ptr_id, dimensions, poids, stock_vente, stock_emprunt, prix_vente, prix_emprunt_par_jour, taux_amende, vendus, empruntes) VALUES
(1, '10x20x5 cm', 1.2, 5, 2, 20.00, 2.00, 0.5, 0, 0),
(2, '15x25x8 cm', 1.5, 4, 1, 25.00, 2.50, 0.2, 0, 0),
(3, '12x18x6 cm', 1.0, 7, 3, 15.00, 1.50, 0.25, 0, 0),
(4, '14x22x7 cm', 1.3, 8, 4, 18.00, 2.00, 0.10, 0, 0),
(5, '11x21x5 cm', 1.1, 6, 2, 22.00, 2.00, 0.60, 0, 0),
(6, '13x23x7 cm', 1.4, 5, 3, 21.00, 1.80, 0.15, 0, 0),
(7, '16x24x8 cm', 1.6, 9, 4, 30.00, 3.00, 0.30, 0, 0),
(8, '10x20x5 cm', 1.2, 10, 5, 25.00, 2.50, 0.25, 0, 0),
(9, '12x22x6 cm', 1.1, 3, 2, 17.00, 1.50, 0.10, 0, 0),
(10, '15x28x7 cm', 1.8, 4, 1, 20.00, 2.20, 0.10, 0, 0);


INSERT INTO "livreNumerique" (livre_ptr_id,path_livre_pdf, prix_vente) VALUES
(1, false, 10.00),
(2,  false, 12.00),
(3, false, 8.00),
(4, false, 11.00),
(6, false, 10.50),
(8, false, 12.50),
(9, false, 7.50),
(10, false, 99.50);


INSERT INTO "livreCategory" (livre_id, category_id) VALUES
(1, 1), -- Fiction
(2, 2), -- Science
(3, 3), -- Technology
(4, 4), -- History
(5, 5), -- Mystery
(6, 6), -- Romance
(7, 7), -- Fantasy
(8, 8), -- Biography
(9, 9), -- Horror
(10, 10); -- Non-fiction



INSERT INTO "livreCategory" (livre_id, category_id) VALUES
(1, 1),  -- Book 1 (Fiction)
(2, 2),  -- Book 2 (Science)
(3, 3),  -- Book 3 (Technology)
(4, 4),  -- Book 4 (History)
(5, 5),  -- Book 5 (Mystery)
(6, 6),  -- Book 6 (Romance)
(7, 7),  -- Book 7 (Fantasy)
(8, 8),  -- Book 8 (Biography)
(9, 9),  -- Book 9 (Horror)
(10, 10); -- Book 10 (Non-fiction)

INSERT INTO commentaire (contenu, utilisateur_id, livre_id) VALUES
('Great book, highly recommended!', 1, 1),
('Interesting read, could be better.', 2, 2),
('Loved the science fiction elements!', 3, 3),
('Very informative and well-researched.', 4, 4),
('A thrilling mystery novel.', 5, 5),
('Romantic and touching.', 6, 6),
('An epic fantasy adventure.', 7, 7),
('A fascinating biography.', 8, 8),
('Spooky and engaging.', 9, 9),
('A must-read for nonfiction lovers.', 10, 10);


INSERT INTO "rating" (utilisateur_id, livre_id, note, date_creation) VALUES
(1, 1, 5, NOW()),
(2, 2, 4, NOW()),
(3, 3, 4, NOW()),
(4, 4, 5, NOW()),
(5, 5, 4, NOW()),
(6, 6, 5, NOW()),
(7, 7, 5, NOW()),
(8, 8, 4, NOW()),
(9, 9, 4, NOW()),
(10, 10, 5, NOW());


INSERT INTO "favoris" (utilisateur_id, livre_id, date_ajout) VALUES
(1, 1, NOW()),
(2, 2, NOW()),
(3, 3, NOW()),
(4, 4, NOW()),
(5, 5, NOW()),
(6, 6, NOW()),
(7, 7, NOW()),
(8, 8, NOW()),
(9, 9, NOW()),
(10, 10, NOW());


INSERT INTO "notification" (utilisateur_id, contenu, type, date_envoi, attachement, read_status) VALUES
(1, 'You have a new book recommendation!', 'book', NOW(), NULL, false),
(2, 'Your favorite book is now available.', 'book', NOW(), NULL, false),
(3, 'A new book has been added to your reading list.', 'book', NOW(), NULL, false),
(4, 'Dont forget to check out our latest books.', 'book', NOW(), NULL, false),
(5, 'Your requested book is now in stock.', 'book', NOW(), NULL, false),
(6, 'A book from your wishlist is on sale.', 'book', NOW(), NULL, false),
(7, 'New books in your favorite category.', 'book', NOW(), NULL, false),
(8, 'Your recommended book is now available for download.', 'book', NOW(), NULL, false),
(9, 'Reminder: Your borrowed book is due soon.', 'reminder', NOW(), NULL, false),
(10, 'Your book has been successfully rented.', 'transaction', NOW(), NULL, false);


INSERT INTO "transaction" (utilisateur_id, livre_id, type, date, montant, type_livre) VALUES
(1, 1, 'achat', NOW(), 20.00, 'physique'),
(2, 2, 'achat', NOW(), 25.00, 'numerique'),
(3, 3, 'emprunt', NOW(), 5.00, 'physique'),
(4, 4, 'achat', NOW(), 15.00, 'numerique'),
(5, 5, 'emprunt', NOW(), 2.00, 'physique'),
(6, 6, 'achat', NOW(), 30.00, 'numerique'),
(7, 7, 'emprunt', NOW(), 3.00, 'physique'),
(8, 8, 'achat', NOW(), 10.00, 'numerique'),
(9, 9, 'emprunt', NOW(), 2.50, 'physique'),
(10, 10, 'achat', NOW(), 12.00, 'numerique');



INSERT INTO "transactionEmprunt" ("transaction_ptr_id", "dateRetour", "dateRetourPrevue") VALUES
(1, CURRENT_DATE, CURRENT_DATE + INTERVAL '7 days'),

(3, CURRENT_DATE, CURRENT_DATE + INTERVAL '7 days'),

(5, CURRENT_DATE, CURRENT_DATE + INTERVAL '7 days'),

(7, CURRENT_DATE, CURRENT_DATE + INTERVAL '7 days'),

(9, CURRENT_DATE, CURRENT_DATE + INTERVAL '7 days');
;


INSERT INTO "facture" (transaction_id, montant, montant_amende, date_creation,path_facture_pdf) VALUES
(1, 20.00, 0.00, NOW(),''),
(2, 25.00, 0.00, NOW(),''),
(3, 5.00, 0.00, NOW(),''),
(4, 15.00, 0.00, NOW(),''),
(5, 2.00, 1.00, NOW(),''),
(6, 30.00, 0.00, NOW(),''),
(7, 3.00, 0.00, NOW(),''),
(8, 10.00, 0.00, NOW(),''),
(9, 2.50, 0.00, NOW(),''),
(10, 12.00, 0.00, NOW(),'');

INSERT INTO demande (utilisateur_id, livre_id, date_demande) VALUES
(1, 1, '2024-12-01 10:00:00'),
(2, 2, '2024-12-02 11:00:00'),
(3, 3, '2024-12-03 12:00:00'),
(4, 4, '2024-12-04 13:00:00'),
(5, 5, '2024-12-05 14:00:00'),
(6, 6, '2024-12-06 15:00:00'),
(7, 7, '2024-12-07 16:00:00'),
(8, 8, '2024-12-08 17:00:00'),
(9, 9, '2024-12-09 18:00:00'),
(10, 10, '2024-12-10 19:00:00');


