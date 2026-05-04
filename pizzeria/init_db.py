from database import SessionLocal, engine, Base
import models.associations
import models.ingrediente
import models.pizza
import models.cliente
import models.ordine
from models.ingrediente import Ingrediente
from models.pizza import Pizza
from models.cliente import Cliente
from models.ordine import Ordine, VocePizzaOrdine, StatoOrdine
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    if db.query(Ingrediente).first():
        print("DB già popolato, esco.")
    else:
        # --- Ingredienti ---
        ingredienti_data = [
            Ingrediente(nome="Pomodoro", prezzo_extra=0.0, allergene=False, vegetariano=True),
            Ingrediente(nome="Mozzarella", prezzo_extra=0.5, allergene=True, vegetariano=True),
            Ingrediente(nome="Basilico", prezzo_extra=0.0, allergene=False, vegetariano=True),
            Ingrediente(nome="Prosciutto Cotto", prezzo_extra=1.0, allergene=False, vegetariano=False),
            Ingrediente(nome="Salamino Piccante", prezzo_extra=1.0, allergene=False, vegetariano=False),
            Ingrediente(nome="Funghi", prezzo_extra=0.5, allergene=False, vegetariano=True),
            Ingrediente(nome="Olive", prezzo_extra=0.5, allergene=False, vegetariano=True),
            Ingrediente(nome="Cipolla", prezzo_extra=0.3, allergene=False, vegetariano=True),
            Ingrediente(nome="Peperoni", prezzo_extra=0.5, allergene=False, vegetariano=True),
            Ingrediente(nome="Wurstel", prezzo_extra=1.0, allergene=True, vegetariano=False),
            Ingrediente(nome="Tonno", prezzo_extra=1.0, allergene=True, vegetariano=False),
            Ingrediente(nome="Gorgonzola", prezzo_extra=1.0, allergene=True, vegetariano=True),
            Ingrediente(nome="Rucola", prezzo_extra=0.5, allergene=False, vegetariano=True),
            Ingrediente(nome="Bresaola", prezzo_extra=1.5, allergene=False, vegetariano=False),
            Ingrediente(nome="Scamorza", prezzo_extra=0.8, allergene=True, vegetariano=True),
        ]
        for i in ingredienti_data:
            db.add(i)
        db.commit()

        # Ricarica ingredienti con ID
        pomodoro = db.query(Ingrediente).filter_by(nome="Pomodoro").first()
        mozzarella = db.query(Ingrediente).filter_by(nome="Mozzarella").first()
        basilico = db.query(Ingrediente).filter_by(nome="Basilico").first()
        prosciutto = db.query(Ingrediente).filter_by(nome="Prosciutto Cotto").first()
        salamino = db.query(Ingrediente).filter_by(nome="Salamino Piccante").first()
        funghi = db.query(Ingrediente).filter_by(nome="Funghi").first()
        olive = db.query(Ingrediente).filter_by(nome="Olive").first()
        cipolla = db.query(Ingrediente).filter_by(nome="Cipolla").first()
        peperoni = db.query(Ingrediente).filter_by(nome="Peperoni").first()
        wurstel = db.query(Ingrediente).filter_by(nome="Wurstel").first()
        tonno = db.query(Ingrediente).filter_by(nome="Tonno").first()
        gorgonzola = db.query(Ingrediente).filter_by(nome="Gorgonzola").first()
        rucola = db.query(Ingrediente).filter_by(nome="Rucola").first()
        bresaola = db.query(Ingrediente).filter_by(nome="Bresaola").first()

        # --- Pizze ---
        pizze_data = [
            Pizza(nome="Margherita", prezzo_base=6.0, descrizione="La classica", disponibile=True,
                  ingredienti=[pomodoro, mozzarella, basilico]),
            Pizza(nome="Marinara", prezzo_base=5.0, descrizione="Pomodoro, aglio, origano", disponibile=True,
                  ingredienti=[pomodoro]),
            Pizza(nome="Diavola", prezzo_base=8.0, descrizione="Con salamino piccante", disponibile=True,
                  ingredienti=[pomodoro, mozzarella, salamino]),
            Pizza(nome="Prosciutto e Funghi", prezzo_base=8.5, descrizione="Classica combinazione", disponibile=True,
                  ingredienti=[pomodoro, mozzarella, prosciutto, funghi]),
            Pizza(nome="Capricciosa", prezzo_base=9.0, descrizione="Completa e saporita", disponibile=True,
                  ingredienti=[pomodoro, mozzarella, prosciutto, funghi, olive]),
            Pizza(nome="Quattro Stagioni", prezzo_base=9.5, descrizione="Quattro gusti in una", disponibile=True,
                  ingredienti=[pomodoro, mozzarella, prosciutto, funghi, olive, cipolla]),
            Pizza(nome="Wurstel e Patatine", prezzo_base=8.0, descrizione="Per i più giovani", disponibile=True,
                  ingredienti=[pomodoro, mozzarella, wurstel]),
            Pizza(nome="Tonno e Cipolla", prezzo_base=8.5, descrizione="Sapore marino", disponibile=True,
                  ingredienti=[pomodoro, mozzarella, tonno, cipolla]),
        ]
        for p in pizze_data:
            db.add(p)
        db.commit()

        # --- Clienti ---
        clienti_data = [
            Cliente(nome="Mario Rossi", telefono="3331234567", indirizzo="Via Roma 1, Milano"),
            Cliente(nome="Giulia Bianchi", telefono="3471234567", indirizzo="Corso Italia 42, Roma"),
            Cliente(nome="Luca Verdi", telefono="3209876543", indirizzo="Via Garibaldi 7, Napoli"),
        ]
        for c in clienti_data:
            db.add(c)
        db.commit()

        # Ricarica
        mario = db.query(Cliente).filter_by(nome="Mario Rossi").first()
        giulia = db.query(Cliente).filter_by(nome="Giulia Bianchi").first()
        luca = db.query(Cliente).filter_by(nome="Luca Verdi").first()

        margherita = db.query(Pizza).filter_by(nome="Margherita").first()
        diavola = db.query(Pizza).filter_by(nome="Diavola").first()
        capricciosa = db.query(Pizza).filter_by(nome="Capricciosa").first()
        quattro = db.query(Pizza).filter_by(nome="Quattro Stagioni").first()
        prosciutto_funghi = db.query(Pizza).filter_by(nome="Prosciutto e Funghi").first()

        ora_base = datetime.now() - timedelta(hours=2)

        # --- Ordini ---
        ordine1 = Ordine(cliente_id=mario.cliente_id, data_ora=ora_base, stato=StatoOrdine.CONSEGNATO, note=None)
        db.add(ordine1)
        db.flush()
        db.add(VocePizzaOrdine(ordine_id=ordine1.ordine_id, pizza_id=margherita.pizza_id, quantita=2))
        db.add(VocePizzaOrdine(ordine_id=ordine1.ordine_id, pizza_id=diavola.pizza_id, quantita=1))

        ordine2 = Ordine(cliente_id=giulia.cliente_id, data_ora=ora_base + timedelta(minutes=30),
                         stato=StatoOrdine.CONSEGNATO, note="Senza cipolla")
        db.add(ordine2)
        db.flush()
        db.add(VocePizzaOrdine(ordine_id=ordine2.ordine_id, pizza_id=capricciosa.pizza_id, quantita=1))

        ordine3 = Ordine(cliente_id=luca.cliente_id, data_ora=ora_base + timedelta(hours=1),
                         stato=StatoOrdine.PRONTO, note=None)
        db.add(ordine3)
        db.flush()
        db.add(VocePizzaOrdine(ordine_id=ordine3.ordine_id, pizza_id=quattro.pizza_id, quantita=2))

        ordine4 = Ordine(cliente_id=mario.cliente_id, data_ora=datetime.now() - timedelta(minutes=45),
                         stato=StatoOrdine.IN_PREPARAZIONE, note="Extra piccante")
        db.add(ordine4)
        db.flush()
        voce4 = VocePizzaOrdine(ordine_id=ordine4.ordine_id, pizza_id=margherita.pizza_id, quantita=1)
        voce4.ingredienti_extra = [salamino, peperoni]
        db.add(voce4)

        ordine5 = Ordine(cliente_id=giulia.cliente_id, data_ora=datetime.now() - timedelta(minutes=10),
                         stato=StatoOrdine.RICEVUTO, note=None)
        db.add(ordine5)
        db.flush()
        db.add(VocePizzaOrdine(ordine_id=ordine5.ordine_id, pizza_id=prosciutto_funghi.pizza_id, quantita=3))

        db.commit()
        print("DB popolato con successo!")

finally:
    db.close()
