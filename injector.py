from tcpgecko import TCPGecko
import time
from Tkinter import *
import tkFileDialog
import os
import struct
import tkMessageBox
from ttk import *
import socket, sys, urllib, urllib2, requests
import webbrowser

import atexit

import py_compile

import os.path
config_exist = os.path.isfile("ip.config") 

from threading import Thread, RLock



scorestreak_ptr = 0x12108AF4

ss_val = [0, 0xC0310000, 0x80310000, 0x00320000, 0x80320000, 0x40320000, 0xC0320000
		 , 0x00330000, 0x40330000, 0xC0330000, 0x00340000, 0x40340000, 0x80340000
		 , 0xC0340000, 0x00350000, 0x40350000, 0x80350000, 0x00360000, 0xC0350000
		 , 0x40360000, 0x80360000, 0xC0360000, 0x00370000]

ss_list = ["None", "Drone", "RC-XD", "Drone de chasse", "Colis strat.", "Drone de brouill.", "Gardien"
			,"Missile hell.", "Foudroiement", "Tourelle auto.", "Machine de mort", "Machine de guerre", "Dragonfire"
			,"Robot terr.", "Aeronef fur.", "Microstation orb.", "Drone d'escorte", "IEM", "Warthog"
			,"Lodestar", "ADAV de Combat", "K9-Unit", "Groupe de chasse"]



verrou = RLock()


Live_DisplayNotification = hex(0x026E27F0 + 0xBAFC0).replace("0x", "0").decode("hex")

s1_ptr = 0x112395AC
s2_ptr = 0x112395B4
s3_ptr = 0x112395B0
name_ptr = 0x121F2C94

freemem = 0x3F000000

f_host = False

tcp = None
f_config = None
r_name = 0

curr_file = {}
curr_inj = 0
base_addr = {}
total_file = 0
old_addr1 = {}
old_addr2 = {}
size_all = {}

temp_vars = []

is_defined_pdt = False


def isnum(c):
	if ord(c) in range(0x30, 0x3a):
		return 1
	else:
		return 0

def isaplha_cap(c):
	if ord(c) in range(65, 91):
		return 1
	else:
		return 0

def isalpha_min(c):
	if ord(c) in range(97, 123):
		return 1
	else:
		return 0

def isalpha(c):
	if isaplha_cap(c) or isalpha_min(c):
		return 1
	else:
		return 0

def detect_cap_n_min(txt):
	min_detected = 0
	cap_detected = 0

	for i in range(0, len(txt)):
		if isalpha(txt[i]):
			if isalpha_min(txt[i]):
				min_detected = 1
			else:
				cap_detected = 1

	if (min_detected + cap_detected) < 2:
		return 0
	else:
		return 1

def float_to_hex(f):
    return hex(struct.unpack('<I', struct.pack('<f', f))[0])

def str_end(string, ind):
	for i in range(0, 0xFFFF):
		x = string[ind+i:ind+i+1:1]
		if x == "\x00":
			return string[ind:ind+i:1]

def dl_res_file():

	webbrowser.open("https://mega.nz/!QFkW1YZa!kEXVkQslsKrKCOPoMkJFRnp2fyUbt70N2m8smI6EF6Y")


def get_changelog():
	url = "http://rambo6glaz.000webhostapp.com/get_changelog.php?x=1"
	r = requests.get(url)
	return r.content
def get_res():
	url = "http://rambo6glaz.000webhostapp.com/get_changelog.php?x=0"
	r = requests.get(url)
	return r.content



def get_news():
	url = "http://rambo6glaz.000webhostapp.com/get_changelog.php?x=2"
	r = requests.get(url)
	buf = r.content
	msg = str_end(buf, 0)
	z = 0 + len(msg) + 1
	link = str_end(buf, z)
	z = z + len(link) + 1
	btn_text = str_end(buf, z)
	return msg, link, btn_text

RES_TEXT = get_res()

NEWS_TEXT, LINK_NEWS, BUTTON = get_news()

CHANGELOG_TEXT = get_changelog()


def open_news():
	webbrowser.open(LINK_NEWS)

def resource():
	pop_up("Resources", RES_TEXT, "Download", dl_res_file)

def connect():
		ip = nip.get()
		global tcp, f_config, inj
		tcp = TCPGecko(ip)
		x = tcp.readmem(name_ptr, 20)
		x = str_end(x, 0)
		print(x)

		tcp.pokemem(0x1076f7a8, 0x000000FF)
		tcp.pokemem(0x027A1794, 0x38600000)

		temp_vars = []
		ShowStats()

		change_text("^2Connected to NexoCube Mod Injector")

		inj.config(state=NORMAL)

		f_config.seek(0, 0)
		f_config.write(ip)
		f_config.close()


def exit_game(msg="You have been banned, no special message."):
	OSFatal = tcp.get_symbol("coreinit.rpl", "OSFatal", True)
	OSAllocFromSystem = tcp.get_symbol("coreinit.rpl", "OSAllocFromSystem", True)
	ret = OSAllocFromSystem(0x400,4)
	tcp.writestr(ret, msg + "\x00")
	OSFatal(ret)
	time.sleep(5)
	sys.exit()

def startGame():

	tcp.pokemem(0x11acae88, 0x01000000)
	tcp.pokemem(0x11acae98, 0x01000000)
	tcp.pokemem(0x11acae80, 0x00000001)
	tcp.pokemem(0x11acaea8, 0x00000001)
	tcp.pokemem(0x11acaebc, 0x00000001)
	tcp.pokemem(0x11acaee0, 0x00000001)

	tcp.pokemem(0x11acaff0 + 0x18, 0x00000001)
	tcp.pokemem(0x11acaff0 + 0x28, 0x00000001)
	tcp.pokemem(0x11acaf90 + 0x18, 0x00000001)
	tcp.pokemem(0x11acaf90 + 0x28, 0x00000001)
	tcp.pokemem(0x11acb8f0 + 0x18, 0x00000001)
	tcp.pokemem(0x11acb8f0 + 0x28, 0x00000001)
	tcp.pokemem(0x11acc0d0 + 0x18, 0x00000001)
	tcp.pokemem(0x11acc0d0 + 0x28, 0x00000001)

	tcp.pokemem(0x11acba10 + 0x18, 0x01010101)
	tcp.pokemem(0x11acba10 + 0x28, 0x01010101)

	
	

	print("You can now start games withtout required players.")

def get_ext_ip():
	x = "https://www.ident.me"
	r = requests.get(x, allow_redirects=True)
	return r.content

def disc():
	with verrou:
		global temp_vars
		temp_vars = []
		change_text("^1Disconnected.")
		tcp.s.close()
		print("Disconnected.")



class changeName_rainbow(Thread):
	global r_name, name, name_ptr

	def __init__(self):
		Thread.__init__(self)

	def run(self):
		with verrou:
			if tcp != None:
				i = 0
				print("Tick/Untick box to use 'Rainbow Name'")
				while r_name == 1:
					if c.get() == 1:
						if i <= 9:
							n_name = "^" + str(i) + name.get()
							i = i + 1
							tcp.writestr(name_ptr, n_name)
							time.sleep(0.5)
						else:
							i = 0
					else:
						sys.exit()


def reset_wiiu():

	with verrou:

		a_v = NORMAL
		b_v = DISABLED

		global inj, res_i, tcp, f_config, r_name, f_host, curr_file, curr_inj, base_addr, total_file, old_addr1, old_addr2, size_all, temp_vars, is_defined_pdt, pdt_names, pdt_clantags, pdt_client_ids, cid_inf_ammo, cid_rapid_fire
		OSForceFullRelaunch = tcp.get_symbol("coreinit.rpl", "OSForceFullRelaunch", True)
		SYSLaunchMenu = tcp.get_symbol("sysapp.rpl", "SYSLaunchMenu", True)
		OSRestartGame = tcp.get_symbol("coreinit.rpl", "OSRestartGame", True)
		#OSForceFullRelaunch()
		OSRestartGame()
		#SYSLaunchMenu()

		inj.config(state=b_v)
		res_i.config(state=b_v)
		tcp = None
		f_config = None
		r_name = 0
		f_host = False
		curr_file = {}
		curr_inj = 0
		base_addr = {}
		total_file = 0
		old_addr1 = {}
		old_addr2 = {}
		size_all = {}

		temp_vars = []

		is_defined_pdt = False

		pdt_names = []
		pdt_clantags = []
		pdt_client_ids = []
		cid_inf_ammo = [0,0,0,0,0,0,0,0,0,0,0,0]
		cid_rapid_fire = [0,0,0,0,0,0,0,0,0,0,0,0]

def shutdown_wiiu():
	OSShutdown = tcp.get_symbol("coreinit.rpl", "OSShutdown", True)
	OSShutdown()

def changeName():
	with verrou:
		global r_name
		var = c.get()

		changeName_reg()


def changeName_reg():
	with verrou:
		n_name = name.get()
		n_name = n_name + "\x00"
		tcp.writestr(name_ptr, n_name)
		print("Name changed !")

def infToken():
	with verrou:
		change_text("^2You now have infinite tokens.")
		tcp.pokemem(0x121079a4, 0x000000FF)

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)

def reset():
	with verrou:
		global curr_inj, total_file, curr_file, base_addr, old_addr1, old_addr2, size_all, inj, res_i
		inj.config(state=NORMAL)
		res_i.config(state=DISABLED)
		print("Free-ing memory (it might take a while)")
		tcp.writestr(freemem, b"\x00"*(curr_inj + 0x100))
		for i in range(0, total_file):
			tcp.pokemem(int(base_addr[i]), int(old_addr1[i], 16))
			tcp.pokemem(int(base_addr[i])+4, int(size_all[i], 16))
			tcp.pokemem(int(base_addr[i])+8, int(old_addr2[i], 16))
			print("De-injected mod " + str(i+1) + " out of " + str(total_file))
		change_text("^2Successfully de-injected.")

def replace_byte(x, n, c):
	shift = (c <<(8*n))
	mask = 0xff << shift
	return (~mask & x)| shift


def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def inject():
	global curr_inj, total_file, curr_file, base_addr, old_addr1, old_addr2, size_all, inj, res_i
	inj.config(state=DISABLED)
	res_i.config(state=NORMAL)
	curr_inj = 0
	total_file = 0
	curr_file = {}
	base_addr = {}
	old_addr1 = {}
	old_addr2 = {}
	size_all = {}
	filename = tkFileDialog.askdirectory()
	parse_gsc_inject(filename)


def inject_mod(base, fname, name, zero_b, zero_a):
	with verrou:
		global curr_inj
		file = open(fname, "rb").read()
		tcp.writestr(freemem + curr_inj, b"\x00"*zero_b)
		tcp.writestr(freemem + curr_inj + zero_b, name.encode('utf-8'))
		tcp.writestr(freemem + curr_inj + zero_b + len(name), b"\x00"*zero_a)
		tcp.writestr(freemem + curr_inj + zero_b + len(name) + zero_a, file)
		tcp.pokemem(base, (freemem + curr_inj + zero_b))
		tcp.pokemem(base+4, len(file))
		tcp.pokemem(base+8, freemem + curr_inj + len(name) + zero_b + zero_a)
		curr_inj += len(file)
		curr_inj = replace_byte(curr_inj, 4, 0) + 0x100

def parse_inject(data, cnt, direct):
	global total_file, curr_file, base_addr, old_addr1, old_addr2, size_all
	file2 = open('final.txt', "r")
	file2.seek(0,0)
	line_cnt = file_len("final.txt")
	c = 0
	for i in range(0, line_cnt):
		line = file2.readline()
		if data[c] in line and c < cnt+1:
			addr1 = file2.readline()
			size = file2.readline()
			addr2 = file2.readline()
			base = int(file2.readline().lstrip().rstrip(), 16)
			base_ = int(hex(base), 16) + 0x10000000
			zero_b = int(file2.readline())
			zero_a = int(file2.readline())
			inject_mod(base_, direct + data[c], data[c], zero_b, zero_a)
			print("Injected file " + str(c+1) + " out of " + str(cnt))
			total_file = total_file + 1
			curr_file[c] = data[c]
			base_addr[c] = base_
			old_addr1[c] = addr1
			old_addr2[c] = addr2
			size_all[c] = size
			c = c+1

def parse_gsc_inject(direct):
	w = {}
	h = 0
	direct = direct + "/"
	for root, dirs, files in os.walk(direct):
		for file in files:
			if file.endswith(".gsc"):
        			x = filename = os.path.join(root, file)
        			x = x.replace("\maps", "maps").replace("\\", "/").replace(direct, "")
        		w[h] = x
        		h = h + 1
	w[h] = "None"
	parse_inject(w, h, direct)


curr_uname = ""


Dvar_FindVar = hex(0x025d0124).replace("0x", "0").decode("hex")
Dvar_SetBool = hex(0x0242B6E8 + 0xBAFC0).replace("0x", "0").decode("hex")
EndGame = hex(0x022E1C10+ 0xBAFC0).replace("0x", "0").decode("hex")
SV_GameSendServerCMD = hex(0x024664A0 + 0xBAFC0).replace("0x", "0").decode("hex")
CBuf_AddText = hex(0x02417D8C + 0xBAFC0).replace("0x", "0").decode("hex")
GiveUAV = hex(0x02757740 + 0xBAFC0).replace("0x", "0").decode("hex")
Dvar_SetInt = 0x02519270 + 0xBAFC0
Dvar_GetBool = 0x02515290 + 0xBAFC0

Dvar_party_connectToOthers = 0x1001F800 + 0x640000 + len("party_connectToOthers")
Dvar_partyMigrate_disabled = 0x1002135C + 0x640000 + len("partyMigrate_disabled")
Dvar_party_mergingEnabled = 0x1001FDEC + 0x640000 + len("party_mergingEnabled")
Dvar_allowAllNAT = 0x100943AC + 0x640000 + len("allowAllNAT")


def find_dvar(str_):
	with verrou:
		OSAllocFromSystem = tcp.get_symbol("coreinit.rpl", "OSAllocFromSystem", True)
		alloc = OSAllocFromSystem(0x20,4)
		tcp.writestr(alloc, str_ + "\x00")
		ret = tcp.call(Dvar_FindVar, alloc)
		return ret

def setDvarBool(dvar, value):
	SV_SendGameServerCommand("set " + dvar + " " + str(value))

PTR_EndGameValue = 0x109264f4

def SV_SendGameServerCommand(cmd):
	with verrou:
		alloc = 0
		if alloc == 0:
			OSAllocFromSystem = tcp.get_symbol("coreinit.rpl", "OSAllocFromSystem", True)
			alloc = OSAllocFromSystem(0x100,4)
		tcp.writestr(alloc, cmd)
		GameEndValue = tcp.readmem(PTR_EndGameValue, 4)
		tcp.call(SV_GameSendServerCMD, 0, 0, alloc)

def print_bo2(msg):
	with verrou:
		SV_SendGameServerCommand("O \"" + msg + "\"")
	
def _Cbuf_AddText(cmd):
	with verrou:
		alloc = 0
		if alloc == 0:
			OSAllocFromSystem = tcp.get_symbol("coreinit.rpl", "OSAllocFromSystem", True)
			alloc = OSAllocFromSystem(0x20,4)
		tcp.writestr(alloc, cmd)
		tcp.call(CBuf_AddText, 0, alloc)


class unlock_dlc_stuff(Thread):

	def __init__(self):
		Thread.__init__(self)

	def run(self):

		print("Unlocking weird stuff.. Wait around 10 seconds :)")

		dvars = ["dlc0"
		, "dlczm0"
		, "dlc0_sale"
		, "dlczm0_sale"
		, "tu_allowDLCWeaponsByOwnership"
		, "ui_showDLCMaps"
		, "ui_isDLCPopupEnabled"
		, "ui_isDLCRequiredPopupEnabled"
		, "ui_DLCPopupDownloadStatusVisible"
		, "SeasonPass"
		, "tu6_enableDLCWeapons"
		, "dlc1"
		, "dlc1_sale"
		, "ui_inGameStoreVisible"]

		for i in range(0, len(dvars)):	
			ret = find_dvar(dvars[i])
			if ret != 0:
				tcp.pokemem(ret + 0x18, 0x01000000)
				tcp.pokemem(ret + 0x28, 0x01000000)


		tcp.pokemem(0x02434cb8 + 0xBAFC0, 0x38600001) #IsDLC0_Included
		tcp.pokemem(0x0243510C + 0xBAFC0, 0x38600001) #DoWeHaveContentPack
		tcp.pokemem(0x02789E4C + 0xBAFC0, 0x38600001) #IsItemDLCAvaible
		tcp.pokemem(0x027577CC + 0xBAFC0, 0x38600000) #UnlockablesDLCWeaponDisabled
		tcp.pokemem(0x024359A4 + 0xBAFC0, 0x38600001)
		tcp.pokemem(0x024332BC + 0xBAFC0, 0x38600001)
		tcp.pokemem(0x024332BC + 0xBAFC0, 0x38600001)
		tcp.pokemem(0x02788CE8 + 0xBAFC0, 0x38600000)
		tcp.pokemem(0x02788CE8 + 0xBAFC0, 0x38600001)
		tcp.pokemem(0x02789EF4 + 0xBAFC0, 0x38600000)
		tcp.pokemem(0x02433F44 + 0xBAFC0, 0x38600000)
		tcp.pokemem(0x0269DF48 + 0xBAFC0, 0x38600001)
		tcp.pokemem(0x0269DF48 + 0xBAFC0, 0x38600001)
		tcp.pokemem(0x0278B110 + 0xBAFC0, 0x38600001)
		tcp.pokemem(0x028E572C + 0xBAFC0, 0x906a0001)

		print("Game patched.")

def unlock():
	thread_unlock = unlock_dlc_stuff()
	thread_unlock.start()

def fix_n(str_):
	if len(str_) == 1:
		str_[1] = "\x00"
		str_[2] = "\x00"
		str_[3] = "\x00"
	if len(str_) == 2:
		str_[2] = "\x00"
		str_[3] = "\x00"
	if len(str_) == 3:
		str_[3] = "\x00"

	return str_

def change_text(t):
	with verrou:
		OSAllocFromSystem = tcp.get_symbol("coreinit.rpl", "OSAllocFromSystem", True)
		alloc = OSAllocFromSystem(0x100, 4)
		tcp.writestr(alloc, t + "\x00")
		tcp.call(Live_DisplayNotification, 0, alloc)

def PushNewStats():

	with verrou:
		global temp_vars

		stats = 0x120FDA40
		Deaths = 0x10A
		Headshots = 0x20C
		Kills = 0x338
		Loses = 0x3AA
		Prestige = 0x7DC
		Rank = 0x7EE
		Score = 0x818
		XP = 0x7F4
		Wins = 0x91A

		n_deaths = 0
		n_hs = 0
		n_kills = 0
		n_loss = 0
		n_prestige = 0
		n_rank = 0
		n_score = 0
		n_wins = 0
		n_xp = 0

		n_deaths = fix_n(struct.pack("<i", int(temp_vars[0].get())))
		n_hs = fix_n(struct.pack("<i", int(temp_vars[1].get())))
		n_kills = fix_n(struct.pack("<i", int(temp_vars[2].get())))
		n_loss = fix_n(struct.pack("<i", int(temp_vars[3].get())))
		n_prestige = fix_n(struct.pack("<i", int(temp_vars[4].get())))
		n_rank = fix_n(struct.pack("<i", int(temp_vars[5].get()) - 1))
		n_score = fix_n(struct.pack("<i", int(temp_vars[6].get())))
		n_wins = fix_n(struct.pack("<i", int(temp_vars[7].get())))
		n_xp = fix_n(struct.pack("<i", int(temp_vars[8].get())))

		data2 = [n_deaths, n_hs, n_kills, n_loss, n_prestige, n_rank, n_score, n_wins, n_xp]
		addr2 = [Deaths, Headshots, Kills, Loses, Prestige, Rank, Score, Wins, XP]

		for i in range(0, len(data2)):
			tcp.writestr(stats + addr2[i], data2[i])

		print("Done.")
		change_text("^2Play one game for the change to take place.")


def ShowStats():
	global temp_vars

	with verrou:

		temp_label = Label(tab4, text="Edit stats :")
		temp_label.grid(row=0, column=0)

		stats = 0x120FDA40
		Deaths = 0x10A
		Headshots = 0x20C
		Kills = 0x338
		Loses = 0x3AA
		Prestige = 0x7DC
		Rank = 0x7EE
		Score = 0x818
		XP = 0x7F4
		Wins = 0x91A
		CLANTAG = 0xBA00
		League = 0x8c5
		PlayTime = 0x8d2

		o_deaths = str(struct.pack("<I", int(str(tcp.readmem(stats + Deaths, 4)).encode("hex"), 16))).encode("hex")
		o_hs = str(struct.pack("<I", int(str(tcp.readmem(stats + Headshots, 4)).encode("hex"), 16))).encode("hex")
		o_kills = str(struct.pack("<I", int(str(tcp.readmem(stats + Kills, 4)).encode("hex"), 16))).encode("hex")
		o_loss = str(struct.pack("<I", int(str(tcp.readmem(stats + Loses, 4)).encode("hex"), 16))).encode("hex")
		o_prestige = str(struct.pack("<B", int(str(tcp.readmem(stats + Prestige, 1)).encode("hex"), 16))).encode("hex")
		o_rank = str(struct.pack("<B", int(str(tcp.readmem(stats + Rank, 1)).encode("hex"), 16)+1)).encode("hex")
		o_score = str(struct.pack("<I", int(str(tcp.readmem(stats + Score, 4)).encode("hex"), 16))).encode("hex")
		o_wins = str(struct.pack("<I", int(str(tcp.readmem(stats + Wins, 4)).encode("hex"), 16))).encode("hex")
		o_xp = str(struct.pack("<I", int(str(tcp.readmem(stats + XP, 4)).encode("hex"), 16))).encode("hex")
		o_time = str(struct.pack("<I", int(str(tcp.readmem(stats + PlayTime, 4)).encode("hex"), 16))).encode("hex")

		label_l = ["Deaths","Headshots","Kills","Loses","Prestige","Rank", "Score", "Wins", "XP", "Time played (s)"]
		label_v = [o_deaths, o_hs, o_kills, o_loss, o_prestige, o_rank, o_score, o_wins, o_xp, o_time]

		for i in range(0, 10):

			temp_label = Label(tab4, text=label_l[i] +": ")
			temp_label.grid(row=i+1, column=0)

			temp_var = StringVar()
			temp_var.set(str(int(label_v[i], 16)))
			temp_vars.append(temp_var)

			temp_entry = Entry(tab4, textvariable=temp_vars[i])
			temp_entry.grid(row=i+1, column=1)

			temp_var = None

		xp_warn = Label(tab4, text="Max: 1249100")
		xp_warn.grid(row=i, column=2)

		dick = Label(tab4, text=" ")
		dick.grid(row=i+2, column=0)

		b_push = Button(tab4, text="Push new stats", command=PushNewStats)
		b_push.grid(row=i+3, column=1)

############## Player Data Table ##############

PlayerState = 0x11239180
Size = 0x5880
Name = 0x5584
ClanTag = 0x55F0
Die = 0x30
Freeze=0x153
VSAT = 0x55D0
Ammo1 = 0x43C
Ammo2 = 0x438
GodMode = Name-0x42
WP_Secondary = 0x2BB
WP_Primary = 0x1BB
Kick = 0x17dc
RapidFire = 0x1D8
ClientNum = 0x1A0

pdt_names = []
pdt_clantags = []
pdt_client_ids = []
cid_inf_ammo = [0,0,0,0,0,0,0,0,0,0,0,0]
cid_rapid_fire = [0,0,0,0,0,0,0,0,0,0,0,0]




def load_pdt():
	global is_defined_pdt, cid_inf_ammo, cid_rapid_fire

	with verrou:

		cid_inf_ammo = [0,0,0,0,0,0,0,0,0,0,0,0]
		cid_rapid_fire = [0,0,0,0,0,0,0,0,0,0,0,0]

		if is_defined_pdt == False:

			for i in range(0, 12):
				name_temp = tcp.readmem(PlayerState + Name + (i*Size), 20)
				pdt_names.append(str_end(name_temp, 0))
			for i in range(0, 12):
				tag_temp = tcp.readmem(PlayerState + ClanTag + (i*Size), 4)
				pdt_clantags.append(tag_temp)
			for i in range(0, 12):
				pdt_client_ids_temp = str(struct.pack(">B", int(str(tcp.readmem(PlayerState + ClientNum + (i*Size), 4)).encode("hex"), 16))).encode("hex")
				pdt_client_ids.append(pdt_client_ids_temp)
				is_defined_pdt = True

		else:

			for i in range(0, 12):
				name_temp = tcp.readmem(PlayerState + Name + (i*Size), 20)
				pdt_names[i] = str_end(name_temp, 0)
			for i in range(0, 12):
				tag_temp = tcp.readmem(PlayerState + ClanTag + (i*Size), 4)
				pdt_clantags[i] = tag_temp
			for i in range(0, 12):
				pdt_client_ids_temp = str(struct.pack(">B", int(str(tcp.readmem(PlayerState + ClientNum + (i*Size), 4)).encode("hex"), 16))).encode("hex")
				pdt_client_ids[i] = pdt_client_ids_temp

		print_pdt()

def print_pdt_debug():
	for i in range(0, 12):
		print("\nClient " + str(i+1) + "\n")
		print("	Name: " + pdt_names[i])
		print("	Clan Tag: " + pdt_clantags[i])

############## Player Data Table ##############

def setDvar_(addr, value):
	with verrou:
		tcp.pokemem(addr + 0x18, value)
		tcp.pokemem(addr + 0x28, value)

############## Non-Host Functions ##############

uav = False
wallhack = False
ssa = False

EveryoneHearsEveryone = 0x110bd974 #0x4C - Off | 0x4D - On
UAV_On = 0x2027CC4  # li r3, 1 # CanLocalPlayerHearActorFootsteps

def do_uav():
	with verrou:
		global uav
		if uav == False:
			tcp.pokemem(UAV_On + 0xBAFC0, 0x38600001)
			change_text("^2UAV ON")
			uav = True
		else:
			tcp.pokemem(UAV_On + 0xBAFC0, 0x38600000)	
			change_text("^1UAV OFF")
			uav = False	


def EnableHBM_Everywhere():
	with verrou:
		EnableHBM = tcp.get_symbol("coreinit.rpl", "OSEnableHomeButtonMenu")
		EnableHBM(1)


def do_ssa():
	with verrou:
		global ssa
		if ssa == False:
			tcp.pokemem(0x0279DDAC + 0xBAFC0, 0x60000000)
			tcp.pokemem(0x0279DD14 + 0xBAFC0, 0x60000000)
			tcp.pokemem(0x0279DE0C + 0xBAFC0, 0x60000000)
			ssa = True
			change_text("^2Super Steady Aim ON")
		else:
			tcp.pokemem(0x0279DDAC + 0xBAFC0, 0x408200D8)
			tcp.pokemem(0x0279DD14 + 0xBAFC0, 0x40820170)
			tcp.pokemem(0x0279DE0C + 0xBAFC0, 0x40820078)
			ssa = False
			change_text("^1Super Steady Aim OFF")


############## Non-Host Functions ##############


root = Tk()
root.title("Black Ops 2 Mod Menu Injector by NexoCube")
note = Notebook(root)

tab1 = Frame(note)
tab2 = Frame(note)
tab3 = Frame(note)
tab4 = Frame(note)
tab5 = Frame(note)
tab6 = Frame(note)
tab7 = Frame(note)

	

########## Tab1 - Injection ##########

bl = Label(tab1, text=" ")
bl.grid(row=0, column = 0)

inj = Button(tab1, text="Inject", width=60, command=inject, compound=CENTER, state=DISABLED)
inj.grid(row=1, column=0)

res_i = Button(tab1, text="De-inject", width=60, command=reset, compound=CENTER)
res_i.grid(row=2, column=0)


res_i.config(state=DISABLED)

########## Tab1 - Injection ##########

########## Tab2 - Host/Conn ##########

blank2 = Label(tab2, text=" ")
blank2.grid(row=0, column = 0)

if config_exist == False:
	nip = StringVar()
	nip.set("Wii U IP Addr")
	f_config = open("ip.config", "a+")
else:
	nip = StringVar()
	f_config = open("ip.config", "r+")
	nip.set(f_config.read())

n_ip = Entry(tab2, textvariable=nip)
n_ip.grid(row=1, column=0)

cnn = Button(tab2, text="Connect", command=connect)
cnn.grid(row=1, column=1)

b_disconnect = Button(tab2, text="Disconnect", command=disc)
b_disconnect.grid(row=1, column=2)


name = StringVar()
name.set("New name")
t_name = Entry(tab2, textvariable=name, width=12)
t_name.grid(row=2, column=1)

b_name = Button(tab2, text="Change name", command=changeName)
b_name.grid(row=2, column=2)

blank2 = Label(tab2, text=" ")
blank2.grid(row=3, column = 0)

reset = Button(tab2, text="Start game", command=startGame)
reset.grid(row=4, column=0)

b_inf_t = Button(tab2, text="Infinite tokens", command=infToken)
b_inf_t.grid(row=4, column=1)

b_weird = Button(tab2, text="Unlock DLC", command=unlock)
b_weird.grid(row=4, column=2)

bl3 = Label(tab2, text=" ")
bl3.grid(row=5, column = 0)

pdt_b = Button(tab2, text="Player Data Table", command=load_pdt)
pdt_b.grid(row=9, column=1)

def fast_restart():
	with verrou:
		_Cbuf_AddText("fast_restart\n")

KillServer = hex(0x02470128 + 0xBAFC0).replace("0x", "0").decode("hex")

def kill_server():
	with verrou:
		tcp.call(KillServer)

antiq = 0

def do_antiquit():
	with verrou:
		antiq = anti_q_v.get()
		if antiq == 1:
			SV_SendGameServerCommand("@ 0")
			antiq = 0
		else:
			SV_SendGameServerCommand("@ 1")
			antiq = 1

def set_map():
	_Cbuf_AddText("map " + new_map_v.get())

blank1337 = Label(tab2, text= " ")
blank1337.grid(row=10, column=0)

fast_restart_b = Button(tab2, text="Fast Restart", command=fast_restart)
fast_restart_b.grid(row=11, column=0)

kill_server_b = Button(tab2, text="Kill Server", command=kill_server)
kill_server_b.grid(row=11, column=1)

anti_q_v = IntVar()
anti_q = Checkbutton(tab2, text="Anti Quit", var=anti_q_v, command=do_antiquit)
anti_q.grid(row=11, column=2)

new_map_v = StringVar()
new_map_v.set("mp_hijacked")
new_map = Entry(tab2, textvariable=new_map_v)
set_map_b = Button(tab2, text="Set Map", command=set_map)
new_map.grid(row=12, column=0)
set_map_b.grid(row=12, column=2)



########## Tab2 - Host/Conn ##########

########## Tab3 - Non-Host. ##########


def set_scorestreak():

	score1_ind = ss_list.index(score1.get())
	score2_ind = ss_list.index(score2.get())
	score3_ind = ss_list.index(score3.get())

	score1_val = ss_val[score1_ind]
	score2_val = ss_val[score2_ind]
	score3_val = ss_val[score3_ind]

	ss_def_value = score1_val + (score2_val >> 8) + (score3_val >> 16)

	tcp.pokemem(scorestreak_ptr, ss_def_value)

def change_fov():
	fov = float_to_hex(float(int(n_fov.get())))
	tcp.pokemem(0x11abdd30+0x18, int(fov, 16))


ssa_v = IntVar()
ssa_b = Checkbutton(tab3, text="Super Steady Aim", command=do_ssa, var=ssa_v)
ssa_b.grid(row=0, column=2)

uav_v = IntVar()
uav_b = Checkbutton(tab3, text="Constant UAV", command=do_uav, var=uav_v)
uav_b.grid(row=0, column=0)

blank18 = Label(tab3, text="")
blank18.grid(row=2, column=0)

enable_hbm = Button(tab3, text="Enable Home Button", command=EnableHBM_Everywhere)
enable_hbm.grid(row=2, column=0)

reset_wiiu_b = Button(tab3, text="Restart Game (temp)", command=reset_wiiu)
reset_wiiu_b.grid(row=2, column=2)

shut_wiiu_b = Button(tab3, text="Shutdown WiiU", command=shutdown_wiiu)
shut_wiiu_b.grid(row=3, column=1)

blank19 = Label(tab3, text="")
blank19.grid(row=4, column=0)

n_fov = StringVar()

c_fov_e = Entry(tab3, textvariable=n_fov)
c_fov_e.grid(row=5, column=0)

c_fov_b = Button(tab3, text="Change FOV", command=change_fov)
c_fov_b.grid(row=5, column=1)

blank47 = Label(tab3, text="")
blank47.grid(row=6, column=0)

score1 = StringVar()
score1.set("None")

score2 = StringVar()
score2.set("None")

score3 = StringVar()
score3.set("None")

score1_list = OptionMenu(tab3, score1, *ss_list)
score1_list.grid(row=7, column=0)

score2_list = OptionMenu(tab3, score2, *ss_list)
score2_list.grid(row=7, column=1)

score3_list = OptionMenu(tab3, score3, *ss_list)
score3_list.grid(row=7, column=2)

score_button = Button(tab3, text="Set Scorestreak", command=set_scorestreak)
score_button.grid(row=8, column=1)

########## Tab3 - Non-Host. ##########

## PDT Functions ##

########## Tab3 - Player DT ##########

client_id = StringVar()



class InfiniteAmmo(Thread):
	def __init__(self, cid, type_pdt):
		Thread.__init__(self)
		self.cid = cid
		self.type = type_pdt

	def run(self):
		
		if self.type == 1:

			while True:

				with verrou:

					t = cid_inf_ammo[self.cid - 1]
					if t == 1:
						tcp.pokemem(PlayerState + Ammo1 + ((self.cid-1)*Size), 0x0000002A)
						tcp.pokemem(PlayerState + Ammo2 + ((self.cid-1)*Size), 0x0000002A)
					else:
						sys.exit()		
		elif self.type == 2:

			while True:

				with verrou:

					t = cid_rapid_fire[self.cid - 1]
					if t == 1:
						tcp.pokemem(PlayerState + RapidFire + ((self.cid-1)*Size), 0x00000000)
					else:
						sys.exit()		


def start_inf_ammo():
	lol = int(client_id.get())
	abcdefg = cid_inf_ammo[lol-1]

	if abcdefg == 0:
		cid_inf_ammo[lol-1] = 1
		thread_inf = InfiniteAmmo(lol, 1)
		thread_inf.start()
		print("Infinite Ammo started for Player with CID " + str(lol))
	else:
		cid_inf_ammo[lol-1] = 0
		print("Infinite Ammo stopped for Player with CID " + str(lol))

def start_rapid_fire():
	lol = int(client_id.get())
	abcdefg = cid_rapid_fire[lol-1]

	if abcdefg == 0:
		cid_rapid_fire[lol-1] = 1
		thread_inf = InfiniteAmmo(lol, 2)
		thread_inf.start()
		print("Rapid Fire started for Player with CID " + str(lol))
	else:
		cid_rapid_fire[lol-1] = 0
		print("Rapid Fire stopped for Player with CID " + str(lol))

def kick_p():
	with verrou:
		print(pdt_client_ids)
		if client_id.get() == "11" or "12":
			client = int(pdt_client_ids[int(client_id.get(), 16) - 1])
		_Cbuf_AddText("banClient " + str(client))

def print_pdt():

	client_list = Label(tab5, text="Client IDS")
	client_list.grid(row=0, column=0)

	client_list = Label(tab5, text="Username")
	client_list.grid(row=0, column=1)

	client_list = Label(tab5, text="Clan-Tag")
	client_list.grid(row=0, column=2)

	for i in range(0,12):

		name_temp = Label(tab5, text=pdt_names[i])
		name_temp.grid(row=i+1, column=1)

		clan_tag_temp = Label(tab5, text=pdt_clantags[i])
		clan_tag_temp.grid(row=i+1, column= 2)

		c_num_temp = Label(tab5, text=str(i+1))
		c_num_temp.grid(row=i+1, column=0)

	text = Label(tab5, text="Type Client Number and click a button")
	text.grid(row=13, column=0)

	client_id.set("lol")
	entry = Entry(tab5, textvariable=client_id)
	entry.grid(row=14, column=0)

	inf_ammo_b = Button(tab5, text="Infinite Ammo", command=start_inf_ammo)
	inf_ammo_b.grid(row=15, column=0)

	rapid_fire_b = Button(tab5, text="Rapid Fire", command=start_rapid_fire)
	rapid_fire_b.grid(row=16, column=0)

	kick_b = Button(tab5, text="Kick", command=kick_p)
	kick_b.grid(row=17, column=0)

	#ClientNames
	#Button(Infinite ammo, rapid fire)


########## Tab3 - Player DT ##########

## PDT Functions ##

########## Tab6 - Nex ID Info ##########

def alloc_struct(size):
	OSAllocFromSystem = tcp.get_symbol("coreinit.rpl", "OSAllocFromSystem", True)
	ret = OSAllocFromSystem(size,4)
	return ret

def alloc_str(msg):
	OSAllocFromSystem = tcp.get_symbol("coreinit.rpl", "OSAllocFromSystem", True)
	ret = OSAllocFromSystem(((len(msg))*2),4)
	tcp.writestr(ret, msg + "\x00\x00")
	return ret

def str_utf8to16(msg):
	out = ""
	for i in range(0, len(msg)):
		temp = "\x00" + msg[i]
		out += temp
		temp = ""
	return out

def change_desc():

	ChangeGameDesc = tcp.get_symbol("nn_fp.rpl", "UpdateGameModeDescription__Q2_2nn2fpFPCw", True)
	ChangeGameMode_N_Desc = tcp.get_symbol("nn_fp.rpl", "UpdateGameMode__Q2_2nn2fpFPCQ3_2nn2fp8GameModePCw", True)
	GetPrincipalId = tcp.get_symbol("nn_fp.rpl", "GetMyPrincipalId__Q2_2nn2fpFv", True)
	IMDisableAPD = tcp.get_symbol("coreinit.rpl", "IMDisableAPD", True)

	msg = n_desc.get()
	ptr = alloc_str(str_utf8to16(msg))
	ChangeGameDesc(ptr)
	IMDisableAPD()

def report_msg():
	url = "http://rambo6glaz.000webhostapp.com/report_message.php?msg="+report_var.get()+"&uname=Free_INJECT"
	r = requests.get(url)
	if "<html>" in r.content:
		print("Server rejected the request, retry.")
	else:
		print("The issue has been reported. You will see the answer once you login again. (If the issue has been resolved.)")

report_var = StringVar()
report_var.set("Suggest idea or report players/bugs. Ask permission to use stuff etc..\n\n\n")

report_l = Entry(tab6, textvariable=report_var, width=40)
report_l.grid(row=0, column=0)

report_b = Button(tab6, text="Report", command=report_msg)
report_b.grid(row=1, column = 0)

n_desc = StringVar()

desc_e = Entry(tab6, textvariable=n_desc)
desc_e.grid(row=4, column=0)

desc_b = Button(tab6, text="Change FL Desc", command=change_desc)
desc_b.grid(row=4, column=1)

about_text = Label(tab7, text="Injector made by NexoCube, relased under the general GNU License.\nDon't act like it is yours, and make sure to give credits.")
about_text.grid(row=1, column=0)

note.add(tab1, text = "Injection")
note.add(tab2, text = "Host")
note.add(tab3, text = "Non-Host")
note.add(tab4, text = "Account")
note.add(tab5, text = "Player Table")
note.add(tab6, text = "NexID")
note.add(tab7, text = "About")
note.pack()
root.mainloop()

