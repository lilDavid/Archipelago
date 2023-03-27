local socket = require("socket")
local json = require('json')
local math = require('math')


local last_modified_date = '2023-03-24' -- Should be the last modified date
local script_version = 0


local gba_wram_start = 0x03000000
local gba_rom_start = 0x08000000

-- array of 36 levels of current states, each represented w/ 32 bits:
--   00000000 00000000 00YYYYYY 00XXXXXX
-- least to most significant: jewel pieces 1234, cd, keyzer
-- X = vanilla save data / AP obtained items
-- Y = AP checked locations
-- 
-- entries congruent 4 mod 6 represent boss rooms
-- - 0x00000008 = door open 
-- - 0x00000020 = boss defeated
local level_status_table = gba_wram_start + 0xA68

-- array of 24 level high scores, divided by 10
local high_scores = gba_wram_start + 0xB10

-- these two together control the game's overall state
local game_mode_addr = gba_wram_start + 0xC3A
local game_state_addr = gba_wram_start + 0xC3C

local wario_health_addr = gba_wram_start + 0x1910

local wario_stop_flag = gba_wram_start + 0x19F6

-- mod stuff
local received_item_count_addr = gba_wram_start + 0xA76

local vanilla_unused_offset = gba_wram_start + 0x6280

local incoming_item_addr = vanilla_unused_offset + 1
local death_link_addr = vanilla_unused_offset + 2

local player_name_addr = gba_rom_start + 0x78F97C

-- convenience functions

-- invert a table (assumes values are unique)
local function invert_table(t)
    local inverted = {}
    for key,val in pairs(t) do
        inverted[val] = key
    end
    return inverted
end

-- a Layout describes how a section of memory is laid out
-- getting a specific data type should return its value,
-- getting a rescursive structure will return the structure with the layout (this is the default behavior)
local Layout = {
    rawget = function(pointer) return pointer.get(pointer) end,
    get = function(pointer) return pointer end,
    set = function(pointer, value) end
}
function Layout:create (l)
    setmetatable(l, self)
    self.__index = self
    return l
end

-- a Layout_Entry gives an offset within the Layout and, recursively, a Layout of memory at that offset
local function Layout_Entry(offset, layout)
    return { offset = offset, layout = layout }
end

local e = Layout_Entry

-- Pointer holds an absolute offset, and has a Layout as its type
local Pointer = {}
function Pointer:new (offset, layout)
    local p = { offset = offset, layout = layout }
    setmetatable(p, Pointer)
    return p
end
function Pointer:cast(layout)
    return Pointer:new(self.offset, layout)
end
function Pointer:rawget(key)
    if not self.layout[key] then
        return self.layout.rawget(self)
    end
    -- get the struct at this entry
    local inner = self.layout[key]
    -- update get the new offset and layout
    local offset = self.offset + inner.offset
    local layout = inner.layout
    -- create a new pointer
    return Pointer:new(offset, layout)
end
function Pointer:get() return self.layout.get(self) end
function Pointer:set(value) return self.layout.set(self, value) end
function Pointer.__index(pointer, key)
    if Pointer[key] then
        return Pointer[key]
    end
    -- get the pointer
    local p = pointer:rawget(key)
    -- resolve the pointer (if the layout is not concrete, it resolves to itself)
    return p:get()
end
function Pointer.__newindex(pointer, key, value)
    -- get the pointer
    local p = pointer:rawget(key)
    -- resolve the pointer (if the layout is not concrete, it resolves to itself)
    p:set(value)
end

-- CONCRETE TYPES

-- Int has a width in bytes to read
local function Int(width)
    local obj = Layout:create {}

    local gets = {
        [1] = function(p)return mainmemory.read_u8(p.offset) end,
        [2] = function(p) return mainmemory.read_u16_be(p.offset) end,
        [3] = function(p) return mainmemory.read_u24_be(p.offset) end,
        [4] = function(p) return mainmemory.read_u32_be(p.offset) end,
    }
    obj.get = gets[width]

    local sets = {
        [1] = function(p, value) mainmemory.write_u8(p.offset, value) end,
        [2] = function(p, value) mainmemory.write_u16_be(p.offset, value) end,
        [3] = function(p, value) mainmemory.write_u24_be(p.offset, value) end,
        [4] = function(p, value) mainmemory.write_u32_be(p.offset, value) end,
    }
    obj.set = sets[width]

    return obj
end

-- alias for types to save space by not creating them multiple times
local Int_8 = Int(1)
local Int_16 = Int(2)
local Int_24 = Int(3)
local Int_32 = Int(4)

-- Bit is a single flag at an address
-- values passed in and returned are booleans
local function Bit(pos)
    local obj = Layout:create {}

    function obj.get(p)
        return bit.check(mainmemory.read_u8(p.offset), pos)
    end

    function obj.set(p, value)
        local orig = mainmemory.readbyte(p.offset)
        local changed
        if value then
            changed = bit.set(orig, pos)
        else
            changed = bit.clear(orig, pos)
        end
        mainmemory.writebyte(p.offset, changed)
    end

    return obj
end

-- Bits is an int that is some mask of bits at the address
-- the range of bit positions is inclusive
local function Bits(start, ending)
    local obj = Layout:create {}

    local mask = 0x00
    for b = start, ending do
        mask = bit.set(mask, b)
    end

    function obj.get(p)
        return bit.rshift( bit.band(mainmemory.read_u8(p.offset), mask), start )
    end

    function obj.set(p, value)
        local orig = mainmemory.readbyte(p.offset)
        orig = bit.band( orig, bit.bnot(mask) )
        mainmemory.writebyte(p.offset, bit.bor(bit.lshift(value, start), orig) )
    end

    return obj
end

local function Value_Named_Layout(layout, lookup)
    local obj = Layout:create {}

    obj.lookup = lookup

    function obj.get(p)
        local value = layout.get(p)
        if lookup[value] then
            value = lookup[value]
        end
        return value
    end

    function obj.rawget(p)
        return layout.get(p)
    end

    local inverse_lookup = invert_table(lookup)

    function obj.set(p, value)
        if type(value) == "string" then
            if inverse_lookup[value] then
                value = inverse_lookup[value]
            else
                return
            end
        end
        layout.set(p, value)
    end

    return obj
end

-- RECURSIVE TYPES

-- holds a list of layouts of a given type, that can be indexed into
-- the Array can be given a list of names for each key to be used as an alternative lookup
local function Array(width, layout, keys)
    local obj = Layout:create {}

    obj.keys = keys

    setmetatable(obj, {
        __index = function(array, key)
            -- allows us to still call get and set
            if Layout[key] then
                return Layout[key]
            end
            -- compute the offset from the start of the array
            if type(key) == "string" then
                if keys[key] then
                    key = keys[key]
                else
                    key = 0
                end
            end
            local offset = key * width
            -- since this is a layout, we are expected to return a layout entry
            return Layout_Entry( offset, layout )
        end
    })

    return obj
end

-- holds a list of bit flags
-- the Bit_Array can be given a list of names for each key to be used as an alternative lookup
local function Bit_Array(bytes, keys)
    local obj = Layout:create {}

    obj.keys = keys

    setmetatable(obj, {
        __index = function(array, key)
            -- allows us to still call get and set
            if Layout[key] then
                return Layout[key]
            end
            -- compute the offset from the start of the array
            if type(key) == "string" then
                if keys[key] then
                    key = keys[key]
                else
                    key = 0
                end
            end
            local byte = bytes - math.floor(key / 8) - 1
            local bit = key % 8
            -- since this is a layout, we are expected to return a layout entry
            return Layout_Entry( byte, Bit(bit) )
        end
    })

    return obj
end

-- a pointer to a specific location in memory
local function Address(layout)
    local obj = Layout:create {}

    function obj.get(p)
        -- get the address
        local address = Int_32.get(p)
        address = bit.band(address, 0x00FFFFFF)
        -- return "Null" for address 0
        if address == 0 then
            return "Null"
        end
        -- create a pointer to it
        return Pointer:new( address, layout )
    end

    function obj.set(p, value)
        -- Null a pointer
        if value == "Null" then
            Int_32.set(p, 0)
            return
        end
        -- assume this is a Pointer
        if type(value) == "table" then
            value = value.offset
        end
        -- create address
        local address =  bit.bor(value, 0x80000000)
        Int_32.set(p, address)
    end

    return obj
end


local level_checks = function(level_name, passage, level)
    local status_address = level_status_table + 24 * passage + 4 * level
    local status_bits = memory.read_u8(status_address + 1)

    local checks = {}
    checks[level_name .. " Jewel Piece Box (Top Right)"] = bit.check(status_bits, 0)
    checks[level_name .. " Jewel Piece Box (Bottom Right)"] = bit.check(status_bits, 1)
    checks[level_name .. " Jewel Piece Box (Bottom Left)"] = bit.check(status_bits, 2)
    checks[level_name .. " Jewel Piece Box (Top Left)"] = bit.check(status_bits, 3)
    checks[level_name .. " CD Box"] = bit.check(status_bits, 4)
    checks[level_name .. " Full Health Item Box"] = bit.check(status_bits, 6)
    return checks
end

local entry_passage_checks = function()
    local checks = {}
    for k, v in pairs(level_checks("Hall of Hieroglyphs", 0, 0)) do checks[k] = v end
    return checks
end

local emerald_passage_checks = function()
    local checks = {}
    for k, v in pairs(level_checks("Palm Tree Paradise", 1, 0)) do checks[k] = v end
    for k, v in pairs(level_checks("Wildflower Fields", 1, 1)) do checks[k] = v end
    for k, v in pairs(level_checks("Mystic Lake", 1, 2)) do checks[k] = v end
    for k, v in pairs(level_checks("Monsoon Jungle", 1, 3)) do checks[k] = v end
    return checks
end

local ruby_passage_checks = function()
    local checks = {}
    for k, v in pairs(level_checks("The Curious Factory", 2, 0)) do checks[k] = v end
    for k, v in pairs(level_checks("The Toxic Landfill", 2, 1)) do checks[k] = v end
    for k, v in pairs(level_checks("40 Below Fridge", 2, 2)) do checks[k] = v end
    for k, v in pairs(level_checks("Pinball Zone", 2, 3)) do checks[k] = v end
    return checks
end

local topaz_passage_checks = function()
    local checks = {}
    for k, v in pairs(level_checks("Toy Block Tower", 3, 0)) do checks[k] = v end
    for k, v in pairs(level_checks("The Big Board", 3, 1)) do checks[k] = v end
    for k, v in pairs(level_checks("Doodle Woods", 3, 2)) do checks[k] = v end
    for k, v in pairs(level_checks("Domino Row", 3, 3)) do checks[k] = v end
    return checks
end

local sapphire_passage_checks = function()
    local checks = {}
    for k, v in pairs(level_checks("Crescent Moon Village", 4, 0)) do checks[k] = v end
    for k, v in pairs(level_checks("Arabian Night", 4, 1)) do checks[k] = v end
    for k, v in pairs(level_checks("Fiery Cavern", 4, 2)) do checks[k] = v end
    for k, v in pairs(level_checks("Hotel Horror", 4, 3)) do checks[k] = v end
    return checks
end

local golden_pyramid_checks = function()
    local checks = {}
    for k, v in pairs(level_checks("Golden Passage", 5, 0)) do checks[k] = v end
    return checks
end

local check_all_locations = function()
    local location_checks = {}
    for k, v in pairs(entry_passage_checks()) do location_checks[k] = v end
    for k, v in pairs(emerald_passage_checks()) do location_checks[k] = v end
    for k, v in pairs(ruby_passage_checks()) do location_checks[k] = v end
    for k, v in pairs(topaz_passage_checks()) do location_checks[k] = v end
    for k, v in pairs(sapphire_passage_checks()) do location_checks[k] = v end
    for k, v in pairs(golden_pyramid_checks()) do location_checks[k] = v end
    return location_checks
end


local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local wl4Socket = nil
local frame = 0

-- Various useful values
local bytes_to_string = function(bytes)
    local string = ''
    for i=0,#(bytes) do
        if bytes[i] == 0 then return string end
        string = string .. string.char(bytes[i])
    end
    return string
end

-- ROM reading and writing functions

-- Reading game state
local function get_current_game_mode()
    return memory.read_u8(game_mode_addr), memory.read_u8(game_state_addr)
end

function InSafeState()
    local mode, state = get_current_game_mode()
    if mode == 2 then
        wario_stopped = memory.read_u16_le(wario_stop_flag) ~= 0
        wario_dying = memory.read_u8(wario_health_addr) == 0
        return state == 2 and (wario_dying or not wario_stopped)
    else
        return mode == 1 and state == 2
    end
end

function item_receivable()
    local itemQueued = memory.read_u8(incoming_item_addr)
    -- Safe to receive an item if the scene is normal and no item is already queued
    return InSafeState() and itemQueued == 0 
end

function get_player_name()
    local name_bytes = memory.readbyterange(player_name_addr, 16)
    return bytes_to_string(name_bytes)
end

function deathlink_enabled()
    local death_link_flag = memory.read_u8(death_link_addr)
    return death_link_flag > 0
end

function get_death_state()
    local mode, _ = get_current_game_mode()
    -- Wario is in a level if he's in mode 2, else he can't really be dead
    if mode ~= 2 then return false end

    local hp_counter = memory.read_u8(wario_health_addr)
    return (hp_counter == 0)
end

function kill_wario()
    memory.write_u8(wario_health_addr, 0)
end

local game_complete = false

local is_game_complete = function()
    mode, status = get_current_game_mode()
    if mode ~= 1 and mode ~= 2 then
        return game_complete
    end

    if game_complete then return true end
    local golden_diva_defeated = false
    local status_bits = memory.read_u32_le(0x3000AF0)
    golden_diva_defeated = status_bits == 0x10

    if (golden_diva_defeated) then
        game_complete = true
        return true
    end

    return false
end

function process_block(block)
    -- Sometimes the block is nothing, if this is the case then quietly stop processing
    if block == nil then
        return
    end
    -- Kill Wario if needed
    if block['triggerDeath'] then
        kill_wario()
    end
    -- Queue item for receiving, if one exists
    item_queue = block['items']
    received_items_count = memory.read_u16_le(received_item_count_addr)
    if received_items_count < #item_queue then
        -- There are items to send: remember lua tables are 1-indexed!
        if item_receivable() then
            memory.write_u8(
                incoming_item_addr,
                bit.bor(item_queue[received_items_count+1], 0x80)
            )
        end
    end
end

-- Main control handling: main loop and socket receive

function receive()
    l, e = wl4Socket:receive()
    -- Handle incoming message
    if e == 'closed' then
        if curstate == STATE_OK then
            print("Connection closed")
        end
        curstate = STATE_UNINITIALIZED
        return
    elseif e == 'timeout' then
        print("timeout")
        return
    elseif e ~= nil then
        print(e)
        curstate = STATE_UNINITIALIZED
        return
    end
    process_block(json.decode(l))

    -- Determine message to send back
    local retTable = {}
    retTable["playerName"] = get_player_name()
    retTable["scriptVersion"] = script_version
    retTable["deathlinkActive"] = deathlink_enabled()
    if InSafeState() then
        retTable["locations"] = check_all_locations()
        retTable["isDead"] = get_death_state()
        retTable["gameComplete"] = is_game_complete()
    end

    -- Send the message
    msg = json.encode(retTable).."\n"
    local ret, error = wl4Socket:send(msg)
    if ret == nil then
        print(error)
    elseif curstate == STATE_INITIAL_CONNECTION_MADE then
        curstate = STATE_TENTATIVELY_CONNECTED
    elseif curstate == STATE_TENTATIVELY_CONNECTED then
        print("Connected!")
        curstate = STATE_OK
    end

end

function main()
    if (is23Or24Or25 or is26To27) == false then
        print("Must use a version of bizhawk 2.3.1 or higher")
        return
    end
    server, error = socket.bind('localhost', 28922)

    while true do
        frame = frame + 1
        if not (curstate == prevstate) then
            prevstate = curstate
        end
        if (curstate == STATE_OK) or (curstate == STATE_INITIAL_CONNECTION_MADE) or (curstate == STATE_TENTATIVELY_CONNECTED) then
            if (frame % 30 == 0) then
                receive()
            end
        elseif (curstate == STATE_UNINITIALIZED) then
            if  (frame % 60 == 0) then
                server:settimeout(2)
                local client, timeout = server:accept()
                if timeout == nil then
                    print('Initial Connection Made')
                    curstate = STATE_INITIAL_CONNECTION_MADE
                    wl4Socket = client
                    wl4Socket:settimeout(0)
                else
                    print('Connection failed, ensure WL4Client is running and rerun wl4_connector.lua')
                    return
                end
            end
        end
        emu.frameadvance()
    end
end

main()