#Git Profile
#https://github.com/DukeOAngels

#License:
#https://github.com/DukeOAngels/Licenses/blob/a19a2fe86a02827b865aaa44a1259ee797b17aba/DukeOAngels%20Demo%20License%20(Strict)

#Script:
#https://github.com/DukeOAngels/MineScript/upload/main/Projects/AutoTool

#Get Minescript_plus at https://github.com/R4z0rX/minescript-scripts/tree/main/Minescript-Plus

import minescript as ms; import ctypes; import time; import pathlib; import json; from java import JavaClass; import minescript_plus as mp

AUTOTOOL_DIR = pathlib.Path(
    r"C:\Users\Byte\AppData\Roaming\ModrinthApp\profiles\Minescript 1.21.8 Fabric\minescript\Duke\autotool" #change your own path to folder where json is stored
)
TOOLS_JSON = AUTOTOOL_DIR / "tools_data.json"
reach = 4.5
chat_outputs = False

TOOL_PRIORITY = {
    "pickaxe": 1,
    "axe": 5,
    "shovel": 3,
    "hoe": 4,
    "sword": 2,
}

HOTBAR_SLOT_DEFAULT = {
    "pickaxe": 2,
    "axe": 1,
    "shovel": 3,
    "hoe": 4,
    "sword": 0,
}

TEMP_SLOT = 35
VK_LBUTTON = 0x01
MINECRAFT_TITLE = "Minecraft"

mc = JavaClass("net.minecraft.client.Minecraft").getInstance()
ClickType = JavaClass("net.minecraft.world.inventory.ClickType")
InventoryScreen = JavaClass("net.minecraft.client.gui.screens.inventory.InventoryScreen")
GameType = JavaClass("net.minecraft.world.level.GameType")

with open(TOOLS_JSON, "r", encoding="utf-8") as f:
    tools_data = json.load(f)

block_lists = {
    "pickaxe": tools_data.get("pickaxe", []),
    "axe": tools_data.get("axe", []),
    "shovel": tools_data.get("shovel", []),
    "hoe": tools_data.get("hoe", []),
    "sword": tools_data.get("sword", []),
}

tool_lists = {
    "pickaxe": tools_data.get("pickaxes", []),
    "axe": tools_data.get("axes", []),
    "shovel": tools_data.get("shovels", []),
    "hoe": tools_data.get("hoes", []),
    "sword": tools_data.get("swords", []),
}

def swap_items(slot1: int, slot2: int):
    container_menu = mc.player.inventoryMenu
    if mc.screen is None:
        mc.setScreen(InventoryScreen(mc.player))
        time.sleep(0.03)
    
    if slot1 < 9:
        mc.gameMode.handleInventoryMouseClick(container_menu.containerId, TEMP_SLOT, slot1, ClickType.SWAP, mc.player)
        mc.gameMode.handleInventoryMouseClick(container_menu.containerId, TEMP_SLOT, slot2, ClickType.SWAP, mc.player)
        mc.gameMode.handleInventoryMouseClick(container_menu.containerId, TEMP_SLOT, slot1, ClickType.SWAP, mc.player)
    else:
        mc.gameMode.handleInventoryMouseClick(container_menu.containerId, slot1, slot2, ClickType.SWAP, mc.player)
        time.sleep(0.02)
        mc.setScreen(None)
        time.sleep(0.02)


user32 = ctypes.windll.user32

def is_minecraft_focused():
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd) + 1
    buffer = ctypes.create_unicode_buffer(length)
    user32.GetWindowTextW(hwnd, buffer, length)
    return MINECRAFT_TITLE in buffer.value

def mode():
    return mc.gameMode.getPlayerMode()

def is_player_free():
    return mc.screen is None

def is_mouse_down():
    return user32.GetAsyncKeyState(VK_LBUTTON) & 0x8000

while True:
    if str(mode()) == 'SURVIVAL' and is_minecraft_focused() and is_player_free():
        if is_mouse_down():
            block = ms.player_get_targeted_block(reach)
            if block:
                block_id = block.type.split("[")[0].split("{")[0].strip()
                best_tool = None
                for tool in sorted(TOOL_PRIORITY, key=lambda t: TOOL_PRIORITY[t]):
                    if TOOL_PRIORITY[tool] == 0:
                        continue
                    if block_id in block_lists[tool]:
                        best_tool = tool
                        break

                if best_tool:
                    found_slot = None
                    found_item_id = None
                    for item_id in reversed(tool_lists[best_tool]):
                        inv_slot = mp.Inventory.find_item(item_id)
                        if inv_slot is not None:
                            found_slot = inv_slot
                            found_item_id = item_id
                            break

                    if found_slot is not None:
                        hotbar_slot = HOTBAR_SLOT_DEFAULT[best_tool]
                        ms.player_inventory_select_slot(hotbar_slot)
                        hands = ms.player_hand_items()
                        current_item = hands.main_hand.get("item") if hands.main_hand else None
                        if current_item != found_item_id:
                            swap_items(found_slot, hotbar_slot)
                            time.sleep(0.05)
                            if is_mouse_down():
                                ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
                                ctypes.windll.user32.mouse_event(0x0001, 0, 0, 0, 0)
                    elif chat_outputs:
                        print(f"No {best_tool} found in inventory!")
                elif chat_outputs:
                    print("No suitable tool!")
    time.sleep(0.01)