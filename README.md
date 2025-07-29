# Mini Webshop - Backend

Ovo je backend dio mini webshop aplikacije napravljen korištenjem FastAPI frameworka u Pythonu.

## 🚀 Pokretanje servera

API je deploy-an na Render. Pošto je korištena besplatna verzija, potrebno je pokrenuti backend (jer se nakon 15 minuta nekorištenja ugasi).
API se pokreće klikom na link: `https://mini-webshop-backend.onrender.com`

API dokumentacija dostupna na:
   - Swagger: `https://mini-webshop-backend.onrender.com/docs`
   - ReDoc: `https://mini-webshop-backend.onrender.com/redoc`

## 📦 Podaci

### Proizvodi

Svaki proizvod sadrži:
- ID
- Naziv
- Opis
- Cijenu
- URL slike
- Količinu
- Datum objave

Podaci se trenutno čuvaju u JSON fajlu (`data/products.json`).

### Narudžbe

Narudžba sadrži:
- ID
- Kupca (ime, prezime, adresa, telefon, email)
- Stavke (ID proizvoda + količina)
- Datum kreiranja
- Status (Prihvaćeno, Odbijeno, Završeno)
- Datum obrade (opcionalno)

## 📮 Endpointi

- `GET /products` — svi proizvodi
- `GET /products/{id}` — pojedinačni proizvod
- `POST /products` — dodavanje proizvoda
- `PUT /products/{id}` — uređivanje proizvoda
- `DELETE /products/{id}` — brisanje

- `GET /orders` — sve narudžbe (filtriranje i sortiranje dostupno)
- `GET /orders/{id}` — jedna narudžba
- `POST /orders` — nova narudžba
- `PATCH /orders/{id}` — promjena statusa narudžbe

## 🔐 Autentikacija

Autentikacija je jednostavno simulirana preko `localStorage` ključa `isAdmin` u frontend aplikaciji. Nema pravih korisničkih računa u backendu ni prave baze podataka za sada, kako je i naglašeno u korisničkim zahtjevima.
