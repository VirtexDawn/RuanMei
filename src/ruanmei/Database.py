import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from peewee import (
    CharField,
    IntegerField,
    Model,
    SqliteDatabase,
    TextField,
)

# Tentukan lokasi app.db dan Schema.json di src/database/
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "app.db"
SCHEMA_PATH = BASE_DIR / "database" / "Schema.json"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)
db = SqliteDatabase(str(DB_PATH))


class JSONField(TextField):
    """Custom Field Peewee untuk konversi otomatis JSON Array/Object di SQLite."""

    def db_value(self, value: Any) -> Optional[str]:
        if value is None:
            return None
        return json.dumps(value, ensure_ascii=False)

    def python_value(self, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, (dict, list)):
            return value
        try:
            return json.loads(value)
        except (ValueError, TypeError):
            return value


class BaseModel(Model):

    class Meta:
        database = db


# ----------------------------------------------------------------------
# ORM MODELS
# ----------------------------------------------------------------------


class Players(BaseModel):
    userid = IntegerField(primary_key=True)  # Primary Key (number)
    id = CharField(unique=True, null=False)  # Unique & NOT NULL (string)
    username = CharField(unique=True, null=False)  # Unique & NOT NULL (string)
    role = IntegerField(null=False, default=0)  # NOT NULL (number)
    inventory = JSONField(null=False, default=list)  # Array JSON []
    statistics = JSONField(null=False, default=dict)  # Object JSON {}

    class Meta:
        table_name = "players"


class Config(BaseModel):
    key = CharField(primary_key=True)  # Dynamic Key (active, bannedids, dll)
    value = JSONField(null=False)  # Stored Value (Boolean, List, Dict, dll)

    class Meta:
        table_name = "config"


# ----------------------------------------------------------------------
# DATABASE INITIALIZATION & MIGRATOR
# ----------------------------------------------------------------------


def InitDatabase() -> None:
    """Melakukan migrasi tabel dan seeding data awal dari Schema.json, mengabaikan $schema."""
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Schema.json tidak ditemukan di {SCHEMA_PATH}"
        )

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        raw_schema = json.load(f)

    # Filter/Abaikan key meta seperti '$schema'
    schema = {k: v for k, v in raw_schema.items() if not k.startswith("$")}

    db.connect(reuse_if_open=True)
    db.create_tables([Players, Config], safe=True)

    # Seed default data dari Schema.json ke tabel config jika belum ada
    if "config" in schema and isinstance(schema["config"], dict):
        for k, default_val in schema["config"].items():
            Config.get_or_create(key=k, defaults={"value": default_val})

    db.close()


# ----------------------------------------------------------------------
# PLAYERS FUNCTIONS (READ & WRITE)
# ----------------------------------------------------------------------


def AddPlayer(
    userid: int,
    custom_id: str,
    username: str,
    role: int = 0,
    inventory: Optional[List] = None,
    statistics: Optional[Dict] = None,
) -> bool:
    """Menambahkan player baru ke database (custom_id menggunakan string)."""
    try:
        db.connect(reuse_if_open=True)
        Players.create(
            userid=userid,
            id=str(custom_id),
            username=username,
            role=role,
            inventory=inventory if inventory is not None else [],
            statistics=statistics if statistics is not None else {},
        )
        return True
    except Exception as e:
        print(f"[Database Error] AddPlayer Failed: {e}")
        return False
    finally:
        db.close()


def GetPlayer(identifier: Union[int, str]) -> Optional[Dict[str, Any]]:
    """Mengambil data player berdasarkan userid (int), custom_id (str), atau username (str)."""
    try:
        db.connect(reuse_if_open=True)
        query = Players.select()

        if isinstance(identifier, int):
            player = query.where(Players.userid == identifier).first()
        else:
            identifier_str = str(identifier)
            player = query.where(
                (Players.id == identifier_str)
                | (Players.username == identifier_str)
            ).first()

        if player:
            return {
                "userid": player.userid,
                "id": player.id,
                "username": player.username,
                "role": player.role,
                "inventory": player.inventory,
                "statistics": player.statistics,
            }
        return None
    finally:
        db.close()


def GetAllPlayers() -> List[Dict[str, Any]]:
    """Mengambil daftar seluruh player."""
    try:
        db.connect(reuse_if_open=True)
        players = Players.select()
        return [
            {
                "userid": p.userid,
                "id": p.id,
                "username": p.username,
                "role": p.role,
                "inventory": p.inventory,
                "statistics": p.statistics,
            }
            for p in players
        ]
    finally:
        db.close()


def UpdatePlayer(userid: int, **kwargs) -> bool:
    """Update field tertentu pada Player."""
    try:
        db.connect(reuse_if_open=True)
        query = Players.update(**kwargs).where(Players.userid == userid)
        updated = query.execute()
        return updated > 0
    except Exception as e:
        print(f"[Database Error] UpdatePlayer Failed: {e}")
        return False
    finally:
        db.close()


def ModifyPlayerInventory(
    userid: int, item: Any, action: str = "add"
) -> bool:
    """Menambah ('add') atau menghapus ('remove') item dari array inventory player."""
    try:
        player_data = GetPlayer(userid)
        if not player_data:
            return False

        inv = player_data["inventory"] or []
        if action == "add":
            inv.append(item)
        elif action == "remove":
            if item in inv:
                inv.remove(item)
            else:
                return False

        return UpdatePlayer(userid, inventory=inv)
    except Exception as e:
        print(f"[Database Error] ModifyPlayerInventory Failed: {e}")
        return False


def UpdatePlayerStatistics(userid: int, stat_key: str, stat_value: Any) -> bool:
    """Mengubah atau menambah atribut di dalam dictionary statistics player."""
    try:
        player_data = GetPlayer(userid)
        if not player_data:
            return False

        stats = player_data["statistics"] or {}
        stats[stat_key] = stat_value

        return UpdatePlayer(userid, statistics=stats)
    except Exception as e:
        print(f"[Database Error] UpdatePlayerStatistics Failed: {e}")
        return False


def DeletePlayer(userid: int) -> bool:
    """Menghapus player dari database berdasarkan userid."""
    try:
        db.connect(reuse_if_open=True)
        query = Players.delete().where(Players.userid == userid)
        deleted = query.execute()
        return deleted > 0
    finally:
        db.close()


# ----------------------------------------------------------------------
# CONFIG FUNCTIONS (READ & WRITE)
# ----------------------------------------------------------------------


def GetConfig(key: str, default: Any = None) -> Any:
    """Membaca nilai konfigurasi berdasarkan key."""
    try:
        db.connect(reuse_if_open=True)
        cfg = Config.get_or_none(Config.key == key)
        return cfg.value if cfg else default
    finally:
        db.close()


def SetConfig(key: str, value: Any) -> bool:
    """Memperbarui atau menambah nilai konfigurasi baru."""
    try:
        db.connect(reuse_if_open=True)
        Config.insert(key=key, value=value).on_conflict_replace().execute()
        return True
    except Exception as e:
        print(f"[Database Error] SetConfig Failed: {e}")
        return False
    finally:
        db.close()


def GetAllConfigs() -> Dict[str, Any]:
    """Mengambil seluruh konfigurasi dalam bentuk dictionary."""
    try:
        db.connect(reuse_if_open=True)
        configs = Config.select()
        return {c.key: c.value for c in configs}
    finally:
        db.close()