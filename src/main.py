from ruanmei import (
    AddPlayer,
    GetAllConfigs,
    GetPlayer,
    InitDatabase,
    ModifyPlayerInventory,
    SetConfig,
    UpdatePlayerStatistics,
    CreateApp,
)

InitDatabase()

AddPlayer(
    userid=12345678,
    custom_id=1,
    username="Virtex",
    role=2,
    inventory=["Sword", "Shield"],
    statistics={"level": 10, "wins": 5},
)

# 3. Manipulasi JSON Inventory & Statistics
ModifyPlayerInventory(userid=12345678, item="Potion", action="add")
UpdatePlayerStatistics(userid=12345678, stat_key="kills", stat_value=42)

# 4. Ambil data player
player = GetPlayer("Virtex")  # Bisa lewat username/userid/id
print("Player Data:", player)

# 5. Baca / Tulis Config
SetConfig("active", True)
print("Config Active:", GetAllConfigs())

CreateApp()