local socket = require("socket")
local json = require('json')
require('common')


local last_modified_date = '2023-08-27' -- Should be the last modified date
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

local incoming_item_addr = gba_wram_start + 0x6281
local incoming_item_exists_addr = gba_wram_start + 0x6282
local incoming_player_addr = gba_wram_start + 0x6283
local death_link_addr = gba_wram_start + 0x6296

local player_name_addr = gba_rom_start + 0x78F97C

local char_map = {
    ['0']=0x00, ['1']=0x01, ['2']=0x02, ['3']=0x03, ['4']=0x04, ['5']=0x05, ['6']=0x06, ['7']=0x07,
    ['8']=0x08, ['9']=0x09, ['A']=0x0a, ['B']=0x0b, ['C']=0x0c, ['D']=0x0d, ['E']=0x0e, ['F']=0x0f,
    ['G']=0x10, ['H']=0x11, ['I']=0x12, ['J']=0x13, ['K']=0x14, ['L']=0x15, ['M']=0x16, ['N']=0x17,
    ['O']=0x18, ['P']=0x19, ['Q']=0x1a, ['R']=0x1b, ['S']=0x1c, ['T']=0x1d, ['U']=0x1e, ['V']=0x1f,
    ['W']=0x20, ['X']=0x21, ['Y']=0x22, ['Z']=0x23, ['a']=0x24, ['b']=0x25, ['c']=0x26, ['d']=0x27,
    ['e']=0x28, ['f']=0x29, ['g']=0x2a, ['h']=0x2b, ['i']=0x2c, ['j']=0x2d, ['k']=0x2e, ['l']=0x2f,
    ['m']=0x30, ['n']=0x31, ['o']=0x32, ['p']=0x33, ['q']=0x34, ['r']=0x35, ['s']=0x36, ['t']=0x37,
    ['u']=0x38, ['v']=0x39, ['w']=0x3a, ['x']=0x3b, ['y']=0x3c, ['z']=0x3d, ['&']=0x3f,
    ['あ']=0x40, ['い']=0x41, ['う']=0x42, ['え']=0x43, ['お']=0x44, ['か']=0x45, ['き']=0x46, ['く']=0x47,
    ['け']=0x48, ['こ']=0x49, ['さ']=0x4a, ['し']=0x4b, ['す']=0x4c, ['せ']=0x4d, ['そ']=0x4e, ['た']=0x4f,
    ['ち']=0x50, ['つ']=0x51, ['て']=0x52, ['と']=0x53, ['な']=0x54, ['に']=0x55, ['ぬ']=0x56, ['ね']=0x57,
    ['の']=0x58, ['は']=0x59, ['ひ']=0x5a, ['ふ']=0x5b, ['へ']=0x5c, ['ほ']=0x5d, ['ま']=0x5e, ['み']=0x5f,
    ['む']=0x60, ['め']=0x61, ['も']=0x62, ['や']=0x63, ['ゆ']=0x64, ['よ']=0x65, ['ら']=0x66, ['り']=0x67,
    ['る']=0x68, ['れ']=0x69, ['ろ']=0x6a, ['わ']=0x6b, ['を']=0x6c, ['ん']=0x6d, ['ぁ']=0x6e, ['ぃ']=0x6f,
    ['ぅ']=0x70, ['ぇ']=0x71, ['ぉ']=0x72, ['ゃ']=0x73, ['ゅ']=0x74, ['ょ']=0x75, ['っ']=0x76, ['が']=0x77,
    ['ぎ']=0x78, ['ぐ']=0x79, ['げ']=0x7a, ['ご']=0x7b, ['ざ']=0x7c, ['じ']=0x7d, ['ず']=0x7e, ['ぜ']=0x7f,
    ['ぞ']=0x80, ['だ']=0x81, ['ぢ']=0x82, ['づ']=0x83, ['で']=0x84, ['ど']=0x85, ['ば']=0x86, ['び']=0x87,
    ['ぶ']=0x88, ['べ']=0x89, ['ぼ']=0x8a, ['ぱ']=0x8b, ['ぴ']=0x8c, ['ぷ']=0x8d, ['ぺ']=0x8e, ['ぽ']=0x8f,
    ['ア']=0x90, ['イ']=0x91, ['ウ']=0x92, ['エ']=0x93, ['オ']=0x94, ['カ']=0x95, ['キ']=0x96, ['ク']=0x97,
    ['ケ']=0x98, ['コ']=0x99, ['サ']=0x9a, ['シ']=0x9b, ['ス']=0x9c, ['セ']=0x9d, ['ソ']=0x9e, ['タ']=0x9f,
    ['チ']=0xa0, ['ツ']=0xa1, ['テ']=0xa2, ['ト']=0xa3, ['ナ']=0xa4, ['ニ']=0xa5, ['ヌ']=0xa6, ['ネ']=0xa7,
    ['ノ']=0xa8, ['ハ']=0xa9, ['ヒ']=0xaa, ['フ']=0xab, ['ヘ']=0xac, ['ホ']=0xad, ['マ']=0xae, ['ミ']=0xaf,
    ['ム']=0xb0, ['メ']=0xb1, ['モ']=0xb2, ['ヤ']=0xb3, ['ユ']=0xb4, ['ヨ']=0xb5, ['ラ']=0xb6, ['リ']=0xb7,
    ['ル']=0xb8, ['レ']=0xb9, ['ロ']=0xba, ['ワ']=0xbb, ['ヲ']=0xbc, ['ン']=0xbd, ['ァ']=0xbe, ['ィ']=0xbf,
    ['ゥ']=0xc0, ['ェ']=0xc1, ['ォ']=0xc2, ['ャ']=0xc3, ['ュ']=0xc4, ['ョ']=0xc5, ['ッ']=0xc6, ['ガ']=0xc7,
    ['ギ']=0xc8, ['グ']=0xc9, ['ゲ']=0xca, ['ゴ']=0xcb, ['ザ']=0xcc, ['ジ']=0xcd, ['ズ']=0xce, ['ゼ']=0xcf,
    ['ゾ']=0xd0, ['ダ']=0xd1, ['ヂ']=0xd2, ['ヅ']=0xd3, ['デ']=0xd4, ['ド']=0xd5, ['バ']=0xd6, ['ビ']=0xd7,
    ['ブ']=0xd8, ['ベ']=0xd9, ['ボ']=0xda, ['パ']=0xdb, ['ピ']=0xdc, ['プ']=0xdd, ['ペ']=0xde, ['ポ']=0xdf,
    ['ヴ']=0xe0, ["'"]=0xe1, [',']=0xe2, ['.']=0xe3, ['ー']=0xe4, ['~']=0xe5, ['…']=0xe6, ['!']=0xe7,
    ['?']=0xe8, ['(']=0xe9, [')']=0xea, ['「']=0xeb, ['」']=0xec, ['『']=0xed, ['』']=0xee, ['[']=0xef,
    [']']=0xf0, ['℃']=0xf1, ['-']=0xf2, [' ']=0xff,
}

local status_words = function()
    local status_address = level_status_table
    local status_words = {}
    for i = 0, 36 do
        table.insert(status_words, memory.read_u32_le(status_address + 4 * i))
    end

    return status_words
end


local STATE_OK = "Ok"
local STATE_TENTATIVELY_CONNECTED = "Tentatively Connected"
local STATE_INITIAL_CONNECTION_MADE = "Initial Connection Made"
local STATE_UNINITIALIZED = "Uninitialized"

local prevstate = ""
local curstate =  STATE_UNINITIALIZED
local wl4Socket = nil
local frame = 0

local utf8_bytes_to_string = function(bytes)
    local string = ''
    for i = 0, #bytes do
        if bytes[i] == 0 then return string end
        string = string .. string.char(bytes[i])
    end
    return string
end

local string_to_wl4_bytes = function(msg)
    local bytes = {}
    for i = 1, #msg do
        local utf = msg:sub(i, i)
        local match = char_map[utf]
        if match == nil then match = 0xFF end

        table.insert(bytes, match)
    end
    return bytes
end

-- Reading game state
local function get_current_game_mode()
    return memory.read_u8(game_mode_addr), memory.read_u8(game_state_addr)
end

function InSafeState()
    local mode, state = get_current_game_mode()
    return (mode == 1 or mode == 2) and state == 2
end

function item_receivable()
    local mode, state = get_current_game_mode()
    local inLevel = mode == 2 and state == 2
    local warioStopped = inLevel and memory.read_u16_le(wario_stop_flag) ~= 0
    local itemQueued = memory.read_u8(incoming_item_exists_addr) ~= 0x00 
    -- Safe to receive an item if the scene is normal, Wario can move, and no item is already queued
    return InSafeState() and not (warioStopped or itemQueued)
end

function get_player_name()
    local name_bytes = memory.readbyterange(player_name_addr, 64)
    return utf8_bytes_to_string(name_bytes)
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
    sender_queue = block['senders']
    name_list = block['playerNames']
    received_items_count = memory.read_u16_le(received_item_count_addr)
    if received_items_count < #item_queue then
        -- There are items to send: remember lua tables are 1-indexed!
        if item_receivable() then
            local player_id = sender_queue[received_items_count+1]
            local player_name
            if player_id == 0 then
                player_name = "Archipelago"
            else
                player_name = name_list[player_id]
            end
            local encoded_name = string_to_wl4_bytes(player_name)
            for i = 17, #encoded_name do
                table.remove(encoded_name, i)
            end
            table.insert(encoded_name, 0xFE)
            memory.write_bytes_as_array(incoming_player_addr, encoded_name)
            memory.write_u8(incoming_item_addr, item_queue[received_items_count+1])
            memory.write_u8(incoming_item_exists_addr, 1)
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
        retTable["itemStatus"] = status_words()
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
    if not checkBizHawkVersion() then
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
                    print('Connection failed, ensure WL4Client is running and rerun connector_wl4.lua')
                    return
                end
            end
        end
        emu.frameadvance()
    end
end

main()