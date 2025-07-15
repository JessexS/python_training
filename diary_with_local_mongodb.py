from pymongo import MongoClient, errors
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re

class DiaryDB:
    
    def __init__(self, connection_string=None):
        if not connection_string:
            connection_string = 'mongodb://localhost:27017/'
        
        try:
            self.client = MongoClient(connection_string)
            self.db = self.client['diary_db']
            self.entries = self.db['db_entries']
            self._create_indexes()
            print("MongoDB-yhteys muodostettu onnistuneesti")
        except errors.ConnectionFailure as e:
            print(f"MongoDB-yhteys epäonnistui: {e}")
    
    def _create_indexes(self):
        try:
            self.entries.create_index([('date', -1)])
            self.entries.create_index([('title', 'text'), ('content', 'text')])
            self.entries.create_index([('tags', 1)])
        except Exception as e:
            print(f"Indeksin luonti epäonnistui: {e}")
    
    def add_entry(self, title, content, tags=None):
        entry = {
            "title": title,
            "content": content,
            "date": datetime.now(),
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "tags": tags or []
        }
        
        try:
            result = self.entries.insert_one(entry)
            return result.inserted_id
        except Exception as e:
            print(f"Merkinnän lisääminen epäonnistui: {e}")
            return None
    
    def get_entry(self, entry_id):
        try:
            from bson.objectid import ObjectId
            return self.entries.find_one({"_id": ObjectId(entry_id)})
        except Exception as e:
            print(f"Merkinnän hakeminen epäonnistui: {e}")
            return None
    
    def get_entries_by_page(self, page=1, entries_per_page=2):
        try:
            skip_count = (page - 1) * entries_per_page
            cursor = self.entries.find().sort("date", -1).skip(skip_count).limit(entries_per_page)
            return list(cursor)
        except Exception as e:
            print(f"Merkintöjen hakeminen epäonnistui: {e}")
            return []
    
    def count_entries(self):
        return self.entries.count_documents({})
    
    def update_entry(self, entry_id, updates):
        try:
            from bson.objectid import ObjectId
            updates["updated_at"] = datetime.now()
            result = self.entries.update_one(
                {"_id": ObjectId(entry_id)},
                {"$set": updates}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Merkinnän päivittäminen epäonnistui: {e}")
            return False
    
    def delete_entry(self, entry_id):
        try:
            from bson.objectid import ObjectId
            result = self.entries.delete_one({"_id": ObjectId(entry_id)})
            return result.deleted_count > 0
        except Exception as e:
            print(f"Merkinnän poistaminen epäonnistui: {e}")
            return False
    
    def close(self):
        if hasattr(self, 'client'):
            self.client.close()
            print("MongoDB-yhteys suljettu")


class DiaryApp:

    def __init__(self, root):
        """Alusta sovellus"""
        self.root = root
        self.root.title("Päiväkirjani")
        self.root.geometry("800x600")
        
        # MongoDB-yhteys
        self.db = DiaryDB()
        
        # Sivutuksen tila
        self.current_page = 1
        self.entries_per_page = 1  # Näytetään yksi merkintä per "sivu"
        self.current_entry_id = None
        
        # Käyttöliittymän alustus
        self.setup_ui()
        
        # Lataa ensimmäinen sivu
        self.load_current_page()
        
        # Sulje MongoDB-yhteys kun sovellus suljetaan
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_ui(self):
        # Pääkehys
        main_frame = tk.Frame(self.root, bg="#f5f5dc")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Kirjan kannet
        book_frame = tk.Frame(main_frame, bg="#8b4513", bd=5, relief=tk.RAISED)
        book_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Kirjan aukeama (vasen ja oikea sivu)
        pages_frame = tk.Frame(book_frame, bg="white")
        pages_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Vasen sivu (merkinnän tiedot)
        self.left_page = tk.Frame(pages_frame, bg="white", width=380)
        self.left_page.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.left_page.pack_propagate(False)  # Estää kehyksen kutistumisen
        
        # Merkinnän otsikko
        self.entry_title = tk.Label(self.left_page, text="", font=("Times New Roman", 16, "bold"), 
                                   bg="white", wraplength=350)
        self.entry_title.pack(pady=(20, 10))
        
        # Merkinnän päivämäärä
        self.entry_date = tk.Label(self.left_page, text="", font=("Times New Roman", 12, "italic"), 
                                  bg="white")
        self.entry_date.pack(pady=5)
        
        # Merkinnän sisältö
        self.entry_content = scrolledtext.ScrolledText(self.left_page, wrap=tk.WORD, 
                                                      font=("Times New Roman", 12),
                                                      width=40, height=15, bg="white")
        self.entry_content.pack(pady=10, fill=tk.BOTH, expand=True)
        self.entry_content.config(state=tk.DISABLED)  # Vain lukuoikeus
        
        # Oikea sivu (toiminnot ja sivunumerot)
        self.right_page = tk.Frame(pages_frame, bg="white", width=380)
        self.right_page.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        self.right_page.pack_propagate(False)  # Estää kehyksen kutistumisen
        
        # Sivunumerot ja navigointi
        nav_frame = tk.Frame(self.right_page, bg="white")
        nav_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        # Edellinen sivu -painike
        self.prev_btn = tk.Button(nav_frame, text="← Edellinen", command=self.previous_page)
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        
        # Sivunumerot
        self.page_label = tk.Label(nav_frame, text="Sivu 1/1", bg="white")
        self.page_label.pack(side=tk.LEFT, padx=10, fill=tk.X, expand=True)
        
        # Seuraava sivu -painike
        self.next_btn = tk.Button(nav_frame, text="Seuraava →", command=self.next_page)
        self.next_btn.pack(side=tk.RIGHT, padx=10)
        
        # Toimintopainikkeet
        btn_frame = tk.Frame(self.right_page, bg="white")
        btn_frame.pack(side=tk.TOP, fill=tk.X, pady=(20, 10))
        
        # Uusi merkintä
        new_btn = tk.Button(btn_frame, text="Uusi merkintä", command=self.new_entry)
        new_btn.pack(pady=5, fill=tk.X)
        
        # Muokkaa merkintää
        edit_btn = tk.Button(btn_frame, text="Muokkaa", command=self.edit_entry)
        edit_btn.pack(pady=5, fill=tk.X)
        
        # Poista merkintä
        delete_btn = tk.Button(btn_frame, text="Poista", command=self.delete_entry)
        delete_btn.pack(pady=5, fill=tk.X)
    
    def load_current_page(self):
        try:
            # Hae merkinnät MongoDB:stä
            entries = self.db.get_entries_by_page(self.current_page, self.entries_per_page)
            total_entries = self.db.count_entries()
            total_pages = max(1, (total_entries + self.entries_per_page - 1) // self.entries_per_page)
            
            # Päivitä sivunumeronäyttö
            self.page_label.config(text=f"Sivu {self.current_page}/{total_pages}")
            
            # Päivitä navigointipainikkeet
            self.prev_btn.config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
            self.next_btn.config(state=tk.NORMAL if self.current_page < total_pages else tk.DISABLED)
            
            # Jos sivulla on merkintä, näytä se
            if entries:
                entry = entries[0]  # Vain ensimmäinen merkintä, jos näytetään 1 per sivu
                self.current_entry_id = str(entry["_id"])
                
                # Päivitä näytettävät tiedot
                self.entry_title.config(text=entry["title"])
                
                # Muotoile päivämäärä suomalaiseen muotoon
                date_str = entry["date"].strftime("%d.%m.%Y %H:%M")
                self.entry_date.config(text=date_str)
                
                # Päivitä sisältö
                self.entry_content.config(state=tk.NORMAL)
                self.entry_content.delete(1.0, tk.END)
                self.entry_content.insert(tk.END, entry["content"])
                self.entry_content.config(state=tk.DISABLED)
            else:
                # Tyhjä sivu
                self.clear_entry_view()
                self.current_entry_id = None
        except Exception as e:
            messagebox.showerror("Virhe", f"Merkintöjen lataaminen epäonnistui: {e}")
    
    def previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.load_current_page()
    
    def next_page(self):
        total_entries = self.db.count_entries()
        total_pages = max(1, (total_entries + self.entries_per_page - 1) // self.entries_per_page)
        
        if self.current_page < total_pages:
            self.current_page += 1
            self.load_current_page()
    
    def clear_entry_view(self):
        self.entry_title.config(text="")
        self.entry_date.config(text="")
        self.entry_content.config(state=tk.NORMAL)
        self.entry_content.delete(1.0, tk.END)
        self.entry_content.config(state=tk.DISABLED)
    
    def new_entry(self):
        entry_window = tk.Toplevel(self.root)
        entry_window.title("Uusi merkintä")
        entry_window.geometry("500x400")
        
        # Otsikko
        tk.Label(entry_window, text="Otsikko:").pack(anchor="w", padx=10, pady=5)
        title_entry = tk.Entry(entry_window, width=50)
        title_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Sisältö
        tk.Label(entry_window, text="Merkintä:").pack(anchor="w", padx=10, pady=5)
        content_text = scrolledtext.ScrolledText(entry_window, wrap=tk.WORD, width=50, height=15)
        content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tagit
        tk.Label(entry_window, text="Tagit (erota pilkulla):").pack(anchor="w", padx=10, pady=5)
        tags_entry = tk.Entry(entry_window, width=50)
        tags_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Tallennuspainike
        def save_entry():
            title = title_entry.get().strip()
            content = content_text.get(1.0, tk.END).strip()
            tags = [tag.strip() for tag in tags_entry.get().split(",") if tag.strip()]
            
            if not title:
                messagebox.showwarning("Varoitus", "Otsikko ei voi olla tyhjä")
                return
                
            if not content:
                messagebox.showwarning("Varoitus", "Merkintä ei voi olla tyhjä")
                return
                            # Tallenna merkintä MongoDB:hen
            entry_id = self.db.add_entry(title, content, tags)
            
            if entry_id:
                messagebox.showinfo("Onnistui", "Merkintä tallennettu!")
                entry_window.destroy()
                
                # Siirry viimeiselle sivulle
                total_entries = self.db.count_entries()
                self.current_page = (total_entries + self.entries_per_page - 1) // self.entries_per_page
                self.load_current_page()
            else:
                messagebox.showerror("Virhe", "Merkinnän tallentaminen epäonnistui")
        
        # Painikkeet
        buttons_frame = tk.Frame(entry_window)
        buttons_frame.pack(pady=10)
        
        save_button = tk.Button(buttons_frame, text="Tallenna", command=save_entry)
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(buttons_frame, text="Peruuta", command=entry_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def edit_entry(self):
        if not self.current_entry_id:
            messagebox.showinfo("Huomautus", "Ei merkintää muokattavana")
            return
            
        # Hae merkintä tietokannasta
        entry = self.db.get_entry(self.current_entry_id)
        if not entry:
            messagebox.showerror("Virhe", "Merkintää ei löydy")
            return
        
        # Luo muokkausikkuna
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Muokkaa merkintää")
        edit_window.geometry("500x400")
        
        # Otsikko
        tk.Label(edit_window, text="Otsikko:").pack(anchor="w", padx=10, pady=5)
        title_entry = tk.Entry(edit_window, width=50)
        title_entry.insert(0, entry["title"])
        title_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Sisältö
        tk.Label(edit_window, text="Merkintä:").pack(anchor="w", padx=10, pady=5)
        content_text = scrolledtext.ScrolledText(edit_window, wrap=tk.WORD, width=50, height=15)
        content_text.insert(tk.END, entry["content"])
        content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Tagit
        tk.Label(edit_window, text="Tagit (erota pilkulla):").pack(anchor="w", padx=10, pady=5)
        tags_entry = tk.Entry(edit_window, width=50)
        tags_entry.insert(0, ", ".join(entry.get("tags", [])))
        tags_entry.pack(fill=tk.X, padx=10, pady=5)
        
        # Päivitysfunktio
        def update_entry():
            title = title_entry.get().strip()
            content = content_text.get(1.0, tk.END).strip()
            tags = [tag.strip() for tag in tags_entry.get().split(",") if tag.strip()]
            
            if not title:
                messagebox.showwarning("Varoitus", "Otsikko ei voi olla tyhjä")
                return
                
            if not content:
                messagebox.showwarning("Varoitus", "Merkintä ei voi olla tyhjä")
                return
            
            # Päivitä MongoDB:ssä
            updates = {
                "title": title,
                "content": content,
                "tags": tags
            }
            
            if self.db.update_entry(self.current_entry_id, updates):
                messagebox.showinfo("Onnistui", "Merkintä päivitetty!")
                edit_window.destroy()
                self.load_current_page()  # Päivitä näkymä
            else:
                messagebox.showerror("Virhe", "Merkinnän päivittäminen epäonnistui")
        
        # Painikkeet
        buttons_frame = tk.Frame(edit_window)
        buttons_frame.pack(pady=10)
        
        save_button = tk.Button(buttons_frame, text="Tallenna", command=update_entry)
        save_button.pack(side=tk.LEFT, padx=5)
        
        cancel_button = tk.Button(buttons_frame, text="Peruuta", command=edit_window.destroy)
        cancel_button.pack(side=tk.LEFT, padx=5)
    
    def delete_entry(self):
        if not self.current_entry_id:
            messagebox.showinfo("Huomautus", "Ei merkintää poistettavana")
            return
            
        # Varmista poisto
        confirm = messagebox.askyesno("Varmista poisto", 
                                     "Haluatko varmasti poistaa tämän merkinnän? Toimintoa ei voi perua.")
        
        if confirm:
            if self.db.delete_entry(self.current_entry_id):
                messagebox.showinfo("Onnistui", "Merkintä poistettu")
                
                # Päivitä näkymä - pysytään samalla sivulla jos mahdollista
                total_entries = self.db.count_entries()
                total_pages = max(1, (total_entries + self.entries_per_page - 1) // self.entries_per_page)
                
                if self.current_page > total_pages:
                    self.current_page = max(1, total_pages)
                
                self.load_current_page()
            else:
                messagebox.showerror("Virhe", "Merkinnän poistaminen epäonnistui")
    
    def on_closing(self):
        try:
            self.db.close()
        except:
            pass
        self.root.destroy()


# Sovelluksen käynnistäminen
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = DiaryApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Sovelluksen käynnistäminen epäonnistui: {e}")
