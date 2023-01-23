from random import choice
import pickle

new_game = True
area_shown = False
swear_jar = 0
game_complete = False
alchemy_puzz_done = False 
alchemy_secret = False
current_zone = None

class PCdata:
	'''Object that stores player data such as the player\'s name,
	 current location, inventory, and event flags.

	 Note that self.is_dead should only be used as a means of ending the
	 game with the player's death, as if it is set to True at any point,
	 the game will proceed to the game over screen.
	 '''
	def __init__(self):
		self.name = ''
		self.current_zone = None
		self.inventory = []

		self.is_dead = False
		self.quit = False 

		self.flag_listing = []
		self.flag_listing_names = []
		self.flag0 = False 	
		self.flag0_name = 'flag0'
		self.flag_listing.append(self.flag0)
		self.flag_listing_names.append(self.flag0_name)
		self.d_table_open = False
		self.d_table_name = 'dining table control'
		self.flag_listing.append(self.d_table_open)
		self.flag_listing_names.append(self.d_table_name)
		self.fireplace = False
		self.fireplace_name = 'fireplace control'
		self.flag_listing.append(self.fireplace)
		self.flag_listing_names.append(self.fireplace_name)
		self.boar_door = False
		self.boar_door_name = 'boar control'
		self.flag_listing.append(self.boar_door)
		self.flag_listing_names.append(self.boar_door_name) 
		self.warden_brick = False 
		self.warden_brick_name = 'brick control'
		self.flag_listing.append(self.warden_brick)
		self.flag_listing_names.append(self.warden_brick_name)
		self.chimera_flag = False
		self.chimera_flag_name = 'chimera life'
		self.flag_listing.append(self.chimera_flag)
		self.flag_listing_names.append(self.chimera_flag_name)
		self.vault_open = False 
		self.v_o_name='vault control'
		self.flag_listing.append(self.vault_open)
		self.flag_listing_names.append(self.v_o_name)
		self.c_crest_open=False
		self.c_c_name='crest door'
		self.flag_listing.append(self.c_crest_open)
		self.flag_listing_names.append(self.c_c_name)
player = PCdata()

class NPC:
	def __init__(self, name, title='', dia0=None, dia1=None, 
				dia2=None, dia3=None, max_dia_cycle=0):
		self.name = name
		self.title = title
		self.current_dia = 0
		self.dia0 = dia0
		self.dia1 = dia1
		self.dia2 = dia2
		self.dia3 = dia3
		self.max_dia_cycle = max_dia_cycle

class Zone:
	'''Object class for individual zones of a map, containing
	 Exits, NPCs, and Objects(interactables).
	'''
	def __init__(self, name,
				npc0='',npc1='',npc2='',npc3='',npc4='',
				obj0='',obj1='',obj2='',obj3='',obj4='',
				look_desc='', in_area=''):

		self.name = name
		self.in_area = in_area
		self.exit0 = None
		self.exit1 = None
		self.exit2 = None
		self.exit3 = None
		self.exit4 = None
		self.all_exits = []
		self.all_exit_names = []
		##############
		self.npc0 = npc0
		self.npc1 = npc1
		self.npc2 = npc2
		self.npc3 = npc3
		self.npc4 = npc4
		self.all_npcs = []
		self.all_npcs_name = []
		##############
		self.all_objs = []
		self.all_objs_name = []
		self.obj0 = obj0
		self.obj1 = obj1
		self.obj2 = obj2
		self.obj3 = obj3
		self.obj4 = obj4

		self.look_desc = look_desc

	def update_atts(self,
				exit0=None,exit1=None, exit2=None,exit3=None,exit4=None,
				npc0=None,npc1=None,npc2=None,npc3=None,npc4=None,
				obj0=None,obj1=None,obj2=None,obj3=None,obj4=None,
				look_desc=None):
		''' Function for updating area information. Each individual
		 exit, NPC, or interact object can be adjusted by specifying its
		 slot and providing the relevant information.'''
		if exit0:
			self.exit0 = exit0
		if exit1:
			self.exit1 = exit1
		if exit2:
			self.exit2 = exit2
		if exit3:
			self.exit3 = exit3
		if exit4:
			self.exit4 = exit4
		# regenerates the list of all exits/exit names
		self.all_exits.clear()
		self.all_exit_names.clear()
		if self.exit0:
			self.all_exit_names.append(self.exit0.name)
			self.all_exits.append(self.exit0)
		if self.exit1:
			self.all_exit_names.append(self.exit1.name)
			self.all_exits.append(self.exit1)
		if self.exit2:
			self.all_exit_names.append(self.exit2.name)
			self.all_exits.append(self.exit2)
		if self.exit3:
			self.all_exit_names.append(self.exit3.name)
			self.all_exits.append(self.exit3)
		if self.exit4:
			self.all_exit_names.append(self.exit4.name)
			self.all_exits.append(self.exit4)


		if npc0:
			self.npc0 = npc0
		if npc1:
			self.npc1 = npc1
		if npc2:
			self.npc2 = npc2
		if npc3:
			self.npc3 = npc3
		if npc4:
			self.npc4 = npc4
		#regenerates the list of npcs/npc names
		self.all_npcs.clear()
		self.all_npcs_name.clear()
		if self.npc0:
			self.all_npcs_name.append(self.npc0.name)
			self.all_npcs.append(self.npc0)
		if self.npc1:
			self.all_npcs_name.append(self.npc1.name)
			self.all_npcs.append(self.npc1)
		if self.npc2:
			self.all_npcs_name.append(self.npc2.name)
			self.all_npcs.append(self.npc2)
		if self.npc3:
			self.all_npcs_name.append(self.npc3.name)
			self.all_npcs.append(self.npc3)
		if self.npc4:
			self.all_npcs_name.append(self.npc4.name)
			self.all_npcs.append(self.npc4)


		if obj0:
			self.obj0 = obj0
		if obj1:
			self.obj1 = obj1
		if obj2:
			self.obj2 = obj2
		if obj3:
			self.obj3 = obj3
		if obj4:
			self.obj4 = obj4
		#regenerates the list of objects/object names
		self.all_objs.clear()
		self.all_objs_name.clear()
		if self.obj0:
			self.all_objs_name.append(self.obj0.name)
			self.all_objs.append(self.obj0)
		if self.obj1:
			self.all_objs_name.append(self.obj1.name)
			self.all_objs.append(self.obj1)
		if self.obj2:
			self.all_objs_name.append(self.obj2.name)
			self.all_objs.append(self.obj2)
		if self.obj3:
			self.all_objs_name.append(self.obj3.name)
			self.all_objs.append(self.obj3)
		if self.obj4:
			self.all_objs_name.append(self.obj4.name)
			self.all_objs.append(self.obj4)

		if look_desc:
			self.look_desc = look_desc

class InvItem:
	def __init__(self, name, order_slot):
		self.name = name
		self.order_slot = order_slot

class InteractObject:
	'''Object class for enviromental objects that can be interacted 
	 with. use_type should be provided as a list, of all actions that
	 may be taken with the specific instance.

	self.name refers to the name of the instance as used by the text
	parser.

	self.description is the text displayed when the player interacts with
	the instance.
	 '''
	def __init__(self, name='', description=''):

		self.name = name 
		self.description = description


class LootBox(InteractObject):
	'''Subclass of InteractObject, for objects which give the player
	 items when opened. Call the "chest" method from the object to
	 give the item to the player.'''
	def __init__(self, name='', description='',item0=None,
				item1=None, item2=None,use_desc='', use_fail_desc=''):
		self.name =name
		self.description=description
		self.item0=item0
		self.item1=item1
		self.item2=item2
		self.was_opened = False
		self.use_desc = use_desc
		self.use_fail_desc = use_fail_desc

	def chest(self):
		if self.was_opened == False:
			print(self.use_desc)
			if self.item0:
				print(f'Obtained the {self.item0.name}')
				player.inventory.append(self.item0)
			if self.item1:
				print(f'Obtained the {self.item1.name}')
				player.inventory.append(self.item1)
			if self.item2:
				print(f'Obtained the {self.item2.name}')
				player.inventory.append(self.item2)
			self.was_opened = True
		else:
			print(self.use_fail_desc)

class SwitchObject(InteractObject):
	'''subclass of InteractObject, used for changing and handling of
	 event flags. Call the switch_use() method to control the flag
	 state.

	 The flag_name attribute is used to specify the flag which
	 the instance controls, and must be a valid flag configured
	 in the player object attributes. Note that flag_name references the
	 name of the target flag in the player.flag_listing_names list.

	 self.use_choice is the dialogue prompt for if the player wishes 
	 to use the object.

	 self.use_desc is the dialogue that plays indicating the object is
	 being used.

	 self.after_use_desc is the dialogue used when examining the object
	 after using it once. For multi-use objects this also serves as the
	 dialogue indicating the object can again.

	 self.not_use_desc is the dialogue used if the player chooses not to
	 interact with the object.

	 self.alt_desc is the alternate description dialogue for use on 
	 alternating uses of a multi use object

	 flag_state_use determines the flag state to be set for single use
	 objects.

	 flag_state_toggle is a boolean which enables an object to be used
	 multiple times if set to True. Note that it is written assuming all
	 flags will start as False.

	 '''
	def __init__(self, name='', description='',
				use_choice='',
				use_desc='', after_use_desc='', not_use_desc='',
				alt_desc='', flag_state_use=True,
				flag_state_toggle=False, flag_name=''):
		self.name = name 
		self.description = description
		self.use_choice = use_choice
		self.use_desc = use_desc
		self.after_use_desc = after_use_desc
		self.not_use_desc = not_use_desc
		self.alt_desc = alt_desc
		self.flag_state_use=flag_state_use
		self.flag_state_toggle = flag_state_toggle
		self.flag_name = flag_name

	def switch_use(self):
		'''Method used to toggle the flag state. Accepts only "yes" as an
		 affirmative answer. Other inputs will be considered negative.'''

		if not self.flag_state_toggle:
			print(self.description)
			if input(f"{self.use_choice}\n").upper() == 'YES':
				print(self.use_desc)
				player.flag_listing[player.flag_listing_names.index(self.flag_name)] = self.flag_state_use
			else:
				print(self.not_use_desc)
				return None
		else:
			if player.flag_listing[player.flag_listing_names.index(self.flag_name)] == False:
				print(self.description)
				if input(f"{self.use_choice}\n").upper() == 'YES':
					print(self.use_desc)
					player.flag_listing[player.flag_listing_names.index(self.flag_name)] = True
				else:
					print(self.not_use_desc)
					return None
			else:
				print(self.alt_desc)
				if input(f"{self.use_choice}\n").upper() == 'YES':
					print(self.after_use_desc)
					player.flag_listing[player.flag_listing_names.index(self.flag_name)] = False
				else:
					print(self.not_use_desc)
					return None

class BarrierObject(InteractObject):
	'''Object class for any object that prevents the player from progressing.
	 This can be anything from a locked door preventing the player from using
	 an exit, a pit that prevents access to an NPC until it is filled, or
	 a wall that must be destroyed to reveal a treasure chest.

	 Call the barrier_open() method to inspect and cross BarrierObject items.

	 Use self.description to set the description given when the player inspects
	 the object before it is crossed.

	 Use self.open_desc to provide a descrption for the object once the player
	 has successfully "passed" it i.e. unlocked a door, filled a pit, etc.
  
	 self.control_flag sets the flag in the player object that controls the
	 "open/closed" state of the object(such as a door being locked, or a 
	 barrier being intact.). If the flag is True, the object will be
	 considered "open". control_flag must reference a flag defined previously
	 in the "player" object, and is given as a string.

	 self.is_key_lock determines if the object requires the player to have
	 a designated "key" item in their inventory. This item can be any item
	 previously defined, and will be removed from the player's inventory
	 after using it to "open" the object.

	 self.lock_key is used to set the "key" required to "open" the object,
	 in concert with self.is_key_lock. lock_key must be set to an instance
	 of an InventoryItem object.

	 self.open_desc sets the description of the object called when the item
	 is in it's "open" state.

	 self.open_text is the description used when "opening" the object, for
	 key-locked objects.

	 self.cannot_open_desc is the text displayed when the player does not
	 have the means to cross the object i.e. lacking a key, a pit which has
	 not been filled in, etc.

	 self.is_choice_cross determines if the player can attempt to cross the
	 barrier before it is "opened".

	 self.choice_prompt is the prompt given to the player asking if they 
	 wish to attempt to cross the barrier, if self.is_choice_cross is True.
	 Accepts "yes" as an affirmative answer and any other input as a
	 negative one.

	 self.not_cross_desc is the description for if the player chooses not
	 to attempt to cross a barrier with is_choice_cross==True.

	 self.do_kill_player determines if the player will die as a result of
	 trying to cross the barrier before "opening" it.

	 self.kill_text is the text to be displayed when the player dies as a
	 result of trying to pass the barrier without the correct item or flag
	 being set.

	 self.zone_to_update determines which zone will be updated to reflect
	 the barrier object being open, and must be specified as a string
	 that represents the name of the target zone. This must be configured
	 in the all_zones and all_zone_names variables.

	 self.zone_new_desc is the updated description to be applied to the
	 target zone.

	 self.do_add_exit determines if a new exit is to be added to the
	 target zone.

	 self.new_exit_num determines which of the 5 exit "slots" the new
	 exit is to be placed in. By default, this will be exit 4(the last
	 in the list). This only needs to be changed if updating the zone
	 an exit goes to.

	 self.new_exit determines which zone the new exit will lead to.
	 Just as with self.zone_to_update, this must be a string representing
	 the name of the target zone.

	 self.do_add_obj determines if a new object is to be added to the
	 target zone.

	 self.new_obj_num determines which of the 5 obj "slots" the new
	 object is to be placed in. By default, this will be obj 4(the last
	 in the list).

	 self.new_obj determines which object will be added to the zone.
	 This must be a string name representation of the object's name.

	 self.do_add_npc determines if a new NPC is added to the zone.

	 self.new_npc_num determines which npc "slot" the new NPC will be
	 added to. This defaults to 4, the "last" slot.

	 self.new_npc sets the NPC to be added, and must be a string name
	 representing the NPC.

	 '''
	def __init__(self, name='', description='',
		control_flag='', is_key_lock=False, lock_key=None, 
		open_desc='', open_text='', cannot_open_desc='',
		is_choice_cross=False, choice_prompt='',
		not_cross_desc='', do_kill_player=False, kill_text='',
		zone_to_update=None, zone_new_desc='',

		do_add_exit=False, new_exit=None,

		do_add_obj=False, new_obj=None,

		do_add_npc=False, new_npc=None
		):
		self.name=name 
		self.description=description
		self.control_flag=control_flag
		self.is_key_lock=is_key_lock
		self.lock_key=lock_key
		self.open_desc=open_desc
		self.open_text=open_text
		self.cannot_open_desc=cannot_open_desc
		self.is_choice_cross=is_choice_cross
		self.choice_prompt=choice_prompt
		self.not_cross_desc=not_cross_desc
		self.do_kill_player=do_kill_player
		self.kill_text=kill_text

		self.zone_to_update=zone_to_update
		self.zone_new_desc=zone_new_desc
		
		self.do_add_exit=do_add_exit
		self.new_exit=new_exit

		self.do_add_obj=do_add_obj
		self.new_obj=new_obj 

		self.do_add_npc=do_add_npc
		self.new_npc=new_npc
		self.is_done = False



	def barrier_open(self):
		if player.flag_listing[player.flag_listing_names.index(self.control_flag)]: 
			print(self.open_desc) 
		else:
			print(self.description)
			if self.is_key_lock:
			 	if self.lock_key in player.inventory:
			 		print(self.open_text)
			 		player.inventory.remove(self.lock_key)
			 		player.flag_listing[player.flag_listing_names.index(self.control_flag)] = True
			 	else:
			 		if not self.is_choice_cross:
				 		print(self.cannot_open_desc)
				 	else:
				 		if input(f"{self.choice_prompt}\n").upper() == 'YES':
				 			if self.do_kill_player:
				 				print(self.kill_text)
				 				player.is_dead = True
				 			else:
				 				print(self.cannot_open_desc)
				 		else:
				 			print(self.not_cross_desc)
			else:
				if not self.is_choice_cross:
					print(self.cannot_open_desc)
				else:
			 		if input(f"{self.choice_prompt}\n").upper() == 'YES':
			 			if self.do_kill_player:
			 				print(self.kill_text)
			 				player.is_dead = True
			 			else:
			 				player.flag_listing[player.flag_listing_names.index(self.control_flag)] = True
			 				print(self.open_text)
			 		else:
			 			print(self.not_cross_desc)
		if player.flag_listing[player.flag_listing_names.index(self.control_flag)] and not self.is_done:
			if self.do_add_exit:
				self.zone_to_update.look_desc += self.zone_new_desc
				self.zone_to_update.exit4 = self.new_exit
				self.zone_to_update.all_exits.append(self.new_exit)
				self.zone_to_update.all_exit_names.append(self.new_exit.name)
			if self.do_add_obj:
				self.zone_to_update.look_desc += self.zone_new_desc
				self.zone_to_update.obj4 = self.new_obj
				self.zone_to_update.all_objs.append(self.new_obj)
				self.zone_to_update.all_objs_name.append(self.new_obj.name)
			if self.do_add_npc:
				self.zone_to_update.look_desc += self.zone_new_desc
				self.zone_to_update.npc4 = self.new_npc 
				self.zone_to_update.all_npcs.append(self.new_npc)
				self.zone_to_update.all_npcs_name.append(self.new_npc.name)
			self.is_done=True

class CodeLock(InteractObject):
	def __init__(self, name='', password='', description='',opening_desc='', fail_desc='',zone_to_update=None,new_exit=None,
		new_desc='', open_desc=''):
		self.name = name
		self.password = password
		self.description = description
		self.open_desc = open_desc
		self.opening_desc = opening_desc
		self.fail_desc = fail_desc
		self.zone_to_update = zone_to_update
		self.locked = True
		self.new_exit = new_exit
		self.new_desc =new_desc	

	def code_lock(self):
		self.p_in = ''
		if self.locked:
			self.p_in = input(self.description)
			if self.password in self.p_in:
				print(self.opening_desc)
				self.locked = False
				self.zone_to_update.exit4=self.new_exit
				self.zone_to_update.all_exit_names.append(self.new_exit.name)
				self.zone_to_update.all_exits.append(self.new_exit)
				self.zone_to_update.look_desc += self.new_desc
			else:
				print(self.fail_desc)
		else:
			print(self.open_desc)
		

class DragonAltar(InteractObject):
	def __init__(self):
		self.name = "DRAGON ALTAR"

	def d_altar(self):
		global game_complete
		self.ruby = 20
		self.emerald = 25
		self.sapphire = 10
		# slot_a = 3
		# slot_b = -3
		# slot_c = 6
		# slot_d = 7
		# slot_e = -4
		self.slots = {'A':3, 'B':-3, 'C':6, 'D':7, 'E':-4}

		self.total_gems = 0
		self.is_clear = False
		self.r_value = 0 			# Oi! Looking in the code
		self.r_slot = None 			# for the solution, eh?
		self.e_value = 0 			# Cheater.
		self.e_slot = None
		self.s_value = 0
		self.s_slot = None
		self.p_quit  = False
		self.p_in = ''
		self.fail_count = 0
		print("You see here a massive golden altar, featuring 5 incredibly lifelike sculptures\n"
			"of dragons in various menacing poses. Each dragon has a letter, from A through E,\n"
			"carved into its forehead, and its mouth sits wide open, as if something can be\n"
			"placed into it. In the center of the altar, you see three brilliantly shining gems\n"
			"set in a triangular shape around a plaque, a Ruby, EMERALD, and SAPPHIRE. In the\n"
			"center of the plaque is an inscription. It reads:\n\n"
			"    \"You who have come this far, we guardian dragons admire your bravery. If the\n"
			"spoils of this castle are what you seek, we present to you a final test of wit.\n"
			"Place the three gemstones you see here into our mouths, and using the magic\n"
			"within, show for how long we have been guarding this castle. Only then will\n"
			"we grant you passage.\"")
		while not self.is_clear and not self.p_quit:
			if self.fail_count >= 5:
				print("As you go to place the orbs, you notice that the dragon with the letter\n"
					"\'C\' engraved into its head\'s eyes are glowing a dull green.")
			if self.fail_count >= 8:
				print("Additionally, the dragon engraved with \'A\' now has brightly glowing\n"
					"red eyes.")
			if self.fail_count > 12:
				print("As if to take pity upon you, the \'E\' dragon\'s eyes now glow a fierce\n"
					"blue, and the \'D\' and \'B\' dragons\' eyes are shining a bright white.")
			while not self.r_value:
				print("Place the RUBY in which dragon\'s mouth?(A/B/C/D/E)")
				self.p_in = input().upper()
				if self.p_in not in ['A','B','C','D','E']:
					print("Sorry, what? Please plainly say where to put the RUBY in i.e. \"A\".")
				else:
					self.r_value = self.ruby * self.slots[self.p_in]
					self.r_slot = self.p_in
					print(f'As you place the RUBY, you see numbers begin to form above the plaque.\n'
						f'As they fade into view, you can see they read as {self.r_value}.')	
			while not self.e_value:
				print("Place the EMERALD in dragon\'s mouth?(A/B/C/D/E)")
				self.p_in = input().upper()
				if self.p_in not in ['A','B','C','D','E'] or self.p_in in self.r_slot:
					print("Sorry, what? Please plainly say where to put the EMERALD in i.e. \"A\".")
				else:
					self.e_value = self.emerald * self.slots[self.p_in]
					self.e_slot = self.p_in
					print(f'Upon placing the EMERALD, you can see the floating number\n'
						f'change to read {self.r_value + self.e_value}.')
			while not self.s_value:
				print("Place the SAPPHIRE in which dragon\'s mouth?(A/B/C/D/E)")
				self.p_in = input().upper()
				if self.p_in not in ['A','B','C','D','E'] or self.p_in in [self.r_slot, self.e_slot]:
					print("Sorry, what? Please plainly say where to put the SAPPHIRE in i.e. \"A\".")
				else:
					self.s_value = self.sapphire * self.slots[self.p_in]
					self.s_slot = self.p_in
			self.total_gems = self.r_value + self.e_value + self.s_value
			print(f"As you place the SAPPHIRE, the numbers shift once again, now reading\n"
				f"as {self.total_gems}.")
			if self.total_gems != 100:
				print("After waiting a few moments, you realize nothing is happening and you have likely\n"
					"made the wrong choice.")
				self.fail_count+=1
				self.p_in = input("Would you like to try again? YES/NO\n").upper()
				if self.p_in == "NO":
					print('You step back from the altar. Perhaps you can find clues to the riddle of the\n'
						'dragons elsewhere in the castle.')
					self.p_quit = True
				else:
					print("You remove the orbs from the dragon\'s mouths, and the floating number slowly\n"
						"vanishes.")
					self.total_gems = 0
					self.r_value = 0
					self.r_slot = None
					self.e_value = 0
					self.e_slot = None
					self.s_value = 0
					self.s_slot = None
					self.p_in = ''
			else:
				input('After a few moments, the floating number shifts and stirs, changing to a message in\n'
					'a language you\'ve never before seen yet somehow understand perfectly:\n\n'
					'\"Wise adventurer, you are the first to ever reach this point. Ever since Anton, lord of this\n'
					'castle perished, we have waited here in solitude for one such as you. Thank you. By\n'
					'claiming the castle treasure, you will free our souls and allow us to rest once more.\"\n\n'
					'Shortly after, the text fades away and you hear a titanic rumbling as the altar splits\n'
					'in half, sliding open to reveal a path forward. The path to the treasure of Castle Dawnstar...')
				self.is_clear = True
		if self.is_clear:
			game_complete = True

class AlchemyPot(InteractObject):
	def __init__(self, name='',description=''):
		self.name = name 
		self.description = description 

	def alch_puzzle(self):
		global game_complete
		global alchemy_puzz_done 
		global alchemy_secret
		self.t_val = 0
		self.wolfroot = 50
		self.dragon_tongue = 300
		self.p_amethyst = 330
		self.p_diamond = 1000
		self.mercury = 71
		self.flame_slug = 25
		self.shroom_powder = 32
		self.deathbloom = 1200
		self.ash_powder = 1300
		self.p_emerald = 800
		self.p_ruby = 790
		self.puz_clear = False 
		self.pl_quit = False
		self.p_in = ''
		self.ing_1 = ''
		self.ing_2 = ''
		self.ing_3 = ''
		self.color = ''
		self.player_ings = [self.ing_1, self.ing_2, self.ing_3]
		self.ing_count = 0
		self.ingredients = {'WOLFROOT':50, 'DRAGON TONGUE':300, 'POWDERED AMETHYST':330,
					'POWDERED DIAMOND':1000,'LIQUID METAL':71, 'EXTRACT OF FLAME SLUG':25,'FELLSHROOM POWDER':32,
					'DEATHBLOOM POLLEN':1200,'ASHEN POWDER':1300,'POWDERED EMERALD':800,'POWDERED RUBY':790}
		self.ing_str = ("The ingredients avaliable to you are as follows:\n"
					" 1. Wolfroot\n"
					" 2. Dragon Tongue\n"
					" 3. Powdered Amethyst\n"
					" 4. Powdered Diamond\n"
					" 5. Liquid Metal\n"
					" 6. Extract of Flame Slug\n"
					" 7. Fellshroom Powder\n"
					" 8. Deathbloom Pollen\n"
					" 9. Ashen Powder\n"
					" 10. Powdered Emerald\n"
					" 11. Powdered Ruby")
		if not alchemy_puzz_done:
			print("This grand cauldron was once used by the castle alchemists for all kinds of\n"
				"magical rituals. It seems like you might be able to use the ingredients here\n"
				"to some extent.")
			if input("Use the alchemy cauldron? (YES/NO) ").upper() != 'YES':
				self.pl_quit = True	
				print("\nYou decide that fiddling with alchemy is not the best idea for now.")
			while not self.puz_clear and not self.pl_quit:
				for ing in self.player_ings:
					while not ing and not self.p_in:
						print(self.ing_str)
						self.p_in = input("Add which ingredient first? (Type the name of the ingredient)").upper()
						if self.p_in not in ["WOLFROOT",'DRAGON TONGUE','POWDERED AMETHYST',
										'POWDERED DIAMOND','LIQUID METAL', 'EXTRACT OF FLAME SLUG',
										'FELLSHROOM POWDER','DEATHBLOOM POLLEN','ASHEN POWDER',
										'POWDERED EMERALD','POWDERED RUBY'] or self.p_in == self.ing_1 or self.p_in==self.ing_2:
							print("Come again? Please enter only the number of the ingredient you wish to add. Remember that\n"
								"you can only use each ingredient once.")
							self.p_in=''
					if self.p_in:
						if self.ing_count == 0:
							self.ing_1 = self.p_in
						elif self.ing_count == 1:
							self.ing_2 = self.p_in
						else:
							self.ing_3=self.p_in
						self.p_in=''
						self.ing_count+=1
				
				
				self.t_val = self.ingredients[self.ing_1] + self.ingredients[self.ing_2] + self.ingredients[self.ing_3]
				if self.t_val in range(0,200):
					self.color = 'red'
				elif self.t_val in range(200,400):
					self.color='orange'
				elif self.t_val in range(400,600):
					self.color='yellow'
				elif self.t_val in range(600,800):
					self.color='green'
					self.puz_clear=True
				elif self.t_val in range(800,1000):
					self.color='blue'
				elif self.t_val in range(1000,1200):
					self.color='indigo'
				elif self.t_val >= 1200 and self.t_val<3000:
					self.color='violet'
				else:
					self.color='white'
					self.puz_clear=True
				print(f"As you add the final ingredient and stir the pot, a sudden cloud of\n"
					f"{self.color} smoke bursts from the cauldron, indicating your completion.")
				if self.color not in ['green','white']:
					print("However, after a few moments, it is clear that nothing happened.")
					if input("Would you like to try again? (YES/NO)").upper() == 'NO':
						self.pl_quit=True
						print("You decide to leave the cauldron alone for now.")
					else:
						for ing in self.player_ings:
							ing = ''
						self.t_val=0
						self.ing_count = 0
				elif self.color=='green':
					self.puz_clear = True
					print("Shortly afterwards, you see beams of green light filling the window\n"
						"of the alchemy laboratory. You feel a magical energy that seems to be\n"
						"pulling on your very soul. Something inside you tells you that this\n"
						"is what you wanted, so you decide to leave the cauldron alone.")
					alchemy_puzz_done = True
				elif self.color=='white':
					self.puz_clear = True
					alchemy_secret = True
		else:
			print("You don\'t need to do anything else with the cauldron.")		

def change_map(targ_map):
	player.current_area = targ_map
	return None

def show_inventory():
	player.inventory.sort(key = lambda item: item.order_slot)
	print("You currently are carrying:")
	for item in player.inventory:
		print(f"-] {item.name} [-")
	return None 

def room_info():
	global area_shown
	print(f'\nYou are in the {current_zone.name},'
		f' in {current_zone.in_area}.\n')
	if not area_shown:
		print(f"\n{current_zone.look_desc}\n")
		area_shown = True
	return None 

def title_menu():
	global new_game
	while not player_in:
		player_in = input("Welcome to Treasure of Castle Dawnstar!\n"
						"Type START to begin the game, LOAD to load a saved game, or QUIT to quit.").upper()
		if "START" in player_in:
			return None
		elif "LOAD" in player_in:
			#load game
			new_game = False
			return None
		elif "QUIT" in player_in:
			player.quit = True
		else:
			print("I don\'t understand. Please type one of START, LOAD, OR QUIT.")
			player_in = ''

intro_text = ("    Castle Dawnstar... built over 200 years ago at the base of Mount Zelva, this\n"
"grand fortress has harbored many a storied leader. None, however, moreso than the\n"
"great warlord, Anton. In his prime, Anton lead a massive subjugation campaign over\n"
"the whole of Empyrea, bringing over seventy percent of the continent under his rule.\n\n"
"    Anton's rule was a brutal one, with his territories frequently being raided for\n"
"food and valuables, and despite the immense unrest this spurred, none were able to\n"
"rise up and break free of his rule. After thirty long years of tyranny, however, an\n"
"unforseen incident occurred, in which Anton was found dead in his own bed, having\n"
"seemingly suffered a silent death overnight. The castle oracle proclaimed this a curse\n"
"brought upon by Anton's iron-fisted rule, and the castle was abandoned overnight.\n\n"
"    To this day, few dare venture into the castle, and those that do never return\n"
"alive. The legends say that Anton\'s grand treasure hoard is still safely locked away\n"
"in the vault, and it is to this end that you make your way to the casle, in search of...\n\n\n\n")

title_card = "THE TREASURE OF CASTLE DAWNSTAR\n\n".center(80) 
about_name = "A game by Reimi\n\n".center(80)			

intro_b = ("As you approach the castle, you feel a sense of unease as you realize how eerily\n"
"quiet the surroundings are, as if all the animals are avoiding this place.\n"
"As you close in, you notice that although the gate is barred, someone has broken\n"
"open a rather large opening in the castle entrance, providing a convienient way\n"
"in.\n\n"
"Dust stirs as you pass through the hole, each footstep tossing a cloud of it into\n"
"the air. The entryway to the castle is utterly massive, and your footsteps echo\n"
"loudly into the distance as you make your way deeper into the entrance hall.")

def game_intro():
	input(intro_text)
	print(title_card)
	print(about_name)
	input(intro_b)

c_entrance = Zone(name='ENTRY HALL',
	look_desc='The entrance hall of Castle Dawnstar, worn with the passage of time. The\n'
			  'doors leading to many areas of the castle are securely locked. You can see\n'
			  'the ENTRANCE to the castle behind you, a WARLORD PAINTING hanging on the far\n'
			  'wall, and many large STATUES around you, as well as the brilliant CASTLE CREST.\n'
			  'VON HARTZ the butler is standing by the pillars.\n'
			  'There are exits to the DINING HALL and the BARRACKS here.',
	in_area = 'THE CASTLE COMMONS')
d_hall = Zone(name= 'DINING HALL',
	look_desc='The grand dining hall of the castle. Once upon a time, the warlord held\n'
			  'incredible feasts, where nobles from around the land would vy for his\n'
			  'favor. You can see the massive DINING TABLE and the grand FIREPLACE here. There\n'
			  'are exits to the KITCHEN and ENTRY HALL here.',
	 in_area='THE CASTLE COMMONS')
kitchen = Zone(name='KITCHEN',
	look_desc='The castle kitchen, where grand feasts of all kinds were once prepared.\n'
			  'Now it is but a shadow of its former self, the remaining food long since\n'
			  'plundered by man and beast alike. Chef CANNA and Chef ABELLO are near the\n'
			  'oven, and you can see a BUTCHER RACK here as well. There are exits to the\n'
			  'DINING HALL and PANTRY here.',
	in_area='THE CASTLE COMMONS')
pantry = Zone(name='PANTRY',
	look_desc='The pantry of the castle, once home to all sorts of ingredients both\n'
			  'domestic and exotic. You can see many containers that once held food, including\n'
			  'POTATO SACKS, TOMATO SACKS, RUM BARRELS, and APPLE BARRELS here. There are also\n'
			  'a number of STRANGE BOXES against the far wall. There is an exit to the KITCHEN\n'
			  'here.',
	in_area='THE CASTLE COMMONS')
barracks = Zone(name='BARRACKS',
	look_desc='Castle Dawnstar\'s barracks, which once housed an impressive army. Most\n'
			  'of the rooms have collapsed, save this one. LOTON the soldier is resting atop a\n'
			  'bunk. In this area, you can see a DUSTY BUNK, a PAINTING, and a COLLAPSED BUNK.\n'
			  'There is an exit to the ENTRY HALL here.',
	in_area='THE CASTLE COMMONS')
s_passage = Zone(name='HIDDEN PASSAGE',
	look_desc='A hidden passage, connecting the castle\'s kitchen and dungeon. There are exits to\n'
			  'the KITCHEN and CELL A here.',
	in_area='THE CASTLE COMMONS')

cell_a = Zone(name='CELL A',
	look_desc='An ordinary unfurnished cell, connected to the kitchen via hidden passage. In\n'
			  'addition to the locked CELL DOOR, you can see a BUCKET here. There is an exit to\n'
			  'the HIDDEN PASSAGE here.',
	in_area='THE CASTLE DUNGEON')
cell_b = Zone(name='CELL B',
	look_desc='This cell is empty, save for the furniture and a FADED JOURNAL atop it. There is an\n'
			  'exit to the DUNGEON CORRIDOR',
	in_area='THE CASTLE DUNGEON')
cell_c = Zone(name='CELL C',
	look_desc='The cell is unusually clean, as if someone lived here just recently. There are some\n'
			  'fresh FOOTPRINTS along the ground, and an oddly clean BUNK against the wall. You can\n'
			  'exit to the DUNGEON CORRIDOR from here.',
	in_area='THE CASTLE DUNGEON')
dun_hall = Zone(name='DUNGEON CORRIDOR',
	look_desc='The hallway of the dungeon, lined with many cells. Most of the cells are\n'
			  'still locked, but a few are missing their doors. You can see several large DRAGON\n'
			  'ORNAMENTS along the walls, as well as a RUSTED CELL and a RUINED DOOR. You can go to\n'
			  'CELL A, CELL B, CELL C, or the WARDEN\'S OFFICE from here.',
	in_area='THE CASTLE DUNGEON')
ward_offc = Zone(name='WARDEN\'S OFFICE',
	look_desc='This office once housed the castle\'s notorious dungeon keeper. In times\n'
			  'past, it was often said that any who were sentenced to the dungeon would,\n' 
			  'meet a sinister end. The furniture belonging to the warden is exquisite,\n'
			  'including a finely crafted oak desk, and a massive bed with a gold-trimmed\n'
			  'frame. The Warden\'s  RED DIARY still rests upon his desk. There is an exit to the\n'
			  'DUNGEON CORRIDOR here.',
	in_area='THE CASTLE DUNGEON')

landing = Zone(name='LANDING',
	look_desc='Atop the stairs from the entrance hall, you can see many exits leading\n'
			  'across the upper floor. A grand stained glass WINDOW rests in the wall, and you can see\n'
			  'a number of PAINTINGS hung here as well. There are exits leading to the AUDIENCE HALL,\n'
			  'LIBRARY, ALCHEMY LAB, and ENTRY HALL here.',
in_area='THE UPPER CASTLE')
aud_hall = Zone(name='AUDIENCE HALL',
	look_desc='The grand hall where the warlord once held audience, from atop his gilded\n'
			  'THRONE. Regal BANNERS are strewn around the room, and you see ANTON the warlord\n'
			  'standing here, looking impatient. There is an exit to the LANDING here.',
	in_area='THE UPPER CASTLE')
library = Zone(name='LIBRARY',
	look_desc='Row upon row of books fill this grand library, where scholars and alchemists\n'
			  'once studied. Even to this day, many of the books remain intact, though the\n'
			  'library itself is in poor shape, its ceiling having buckled and collapsed in\n'
			  'several places. A HISTORY BOOK and CASTLE HISTORY book lie open on a table here,\n'
			  'along with a nearby GEM BOOK. A grand CHANDELIER has crashed on the floor, and a\n'
			  'particularly odd BOOKSHELF catches your eye. You can see exits to the STUDY and LANDING here.',
	in_area='THE UPPER CASTLE')
study = Zone(name='STUDY',
	look_desc='A personal study belonging to the castle\'s past owner. An odd LANTERN on the\n'
			  'DESK fills the room with a soft glow. You can see ALBERT the alchemist waiting\n'
			  'by the exit back to the LIBRARY, near a rather ODD BOOKSHELF.',
	in_area='THE UPPER CASTLE')
vault = Zone(name='VAULT',
	look_desc='This must be it! The entrance to the vault that holds the fortune of Castle\n'
			  'Dawnstar! In the distance, you can see a DRAGON ALTAR, perhaps a key to the\n'
			  'treasure chamber? However, you can also see a massive CHIMERA resting in\n'
			  'the center of the room... You can also go back to the LIBRARY from here.',
in_area='THE UPPER CASTLE')
a_lab = Zone(name='ALCHEMY LAB',
	look_desc='At one time, this laboratory was used by the court alchemists to create all\n'
			  'kinds of magical creations, both fair and foul. Now, it lies in ruins, though\n'
			  'the component STORAGE seem to be partially intact. The alchemists\' CAULDRON\n'
			  'and NOTES remain undamaged, as well. The nearby doorway leads back to the\n'
			  'LANDING.',
	in_area='THE UPPER CASTLE')

v_hartz = NPC(name='VON HARTZ', title='THE BUTLER',
			dia0='Oh my, a living being? We rarely get those anymore. Ah, but, forgive my\n'
			 'rudeness. I am Von Hartz, head butler of Castle Dawnstar. As you can see, I am\n'
			 'dead. In fact, all of us are. You see, our master did not wish his secret\n'
			 'treasure to be claimed even in death, so he created a powerful binding spell,\n'
			 'binding us here long after our own deaths. It\'s quite a bother, really.',
			dia1='Ah, so you also seek the treasure? Though I do not know where it lies,\n'
			 'I can tell you that you will most likely wish to find a way to the upper\n'
			 'floor. The Master was quite fond of magical locks, you see, so many of the\n'
			 'passageways throughout the castle are sealed.', 
			dia2='Why am I helping you, you ask? Well, you see, being bound to a decrepit\n'
				 'old castle like this for a hundred and fifty years is quite dull. At this\n'
				 'point, I\'d simply like to move on to the afterlife, a sentiment that most\n'
				 'of the castle\'s residents share, you\'ll find.',
			max_dia_cycle=2)

c_canna = NPC(name='CANNA', title='THE CHEF',
			dia0='Oh, an adventurer seeking the castle\'s treasure, eh? Interesting. Well,\n'
			  'if it\'s the treasure you seek, you should know that our lord was quite fond of\n'
			  'using his favorite foods in locks around the castle.',
			dia1='Our lord\'s favorite foods? Unfortunately, I\'ve rather forgotten over the\n'
			  'years, and all I can remember these days is that he was rather fond of a fruit.', 
			dia2='Honestly, you might be better off asking Abello about this, his memory was\n'
				'always sharper than.... huh? Sorry, who are you again?', 
			max_dia_cycle=2)

c_abello = NPC(name='ABELLO', title='THE CHEF',
				dia0='Another dogged contender seeks the treasure, eh? Very well. As Canna may\n'
				'have already informed you, our lord was quite fond of his food.',
				dia1='Our lord\'s favorite food? Well, all I can remember is that he was quite\n'
				'fond of \'drinking the blood of his enemies\', as he would say.', 
				dia2='...I feel like I\'ve forgotten something horrible, though I cannot say what.\n',
				max_dia_cycle=2)

s_loton = NPC(name='LOTON', title='THE SOLDIER',
			dia0='Ah, an adventurer! Another one into the meat grinder, eh?',
			dia1='What, why so serious? I\'ve only seen dozens of self-proclaimed \'Treasure\n'
			'Hunters\' like yourself send themselves to a messy demise over the years.', 
			dia2='It\'s that blasted beast upstairs what does it, you see. The accursed thing\n'
			'can only be harmed by silver weapons, but silver is long since gone from this land\n'
			'nowadays, so it may as well be immortal.',
			dia3='Listen, some honest advice from me to you... if you encounter that... thing...\n'
			'don\'t take any chances with it unless you have some kind of silver on you. That\'s\n'
			'the only way you have even a chance at killing it.', max_dia_cycle=3)

a_anton = NPC(name='ANTON', title='THE WARLORD',
			dia0='Aha! Thank you, brave one, for running that blasted bandit out of here. The fool\n'
			'had been treating my majestic castle like his own little hideout, and with the whole\n'
			'\'being a ghost\' thing, I couldn\' do anything about it!',
			dia1='Hm? You\'re seeking my treasure...? Ah. Well... it\'s been a long time. Ever since\n'
			'my soulbinding ritual went sour, I\'ve been trapped here with my men. It gets rather tiring\n'
			'after fifty years or so... Yes, even us ghosts get tired! Bwahaha!', 
			dia2='Hmm... well, I can tell you where the treasure is, but you must do me a favor in.\n'
			'exchange. Please... go to the castle\'s alchemy lab, and reverse my accursed soulbinding.\n'
			'I was a fool... and my men deserve to rest. The treasure vault is hidden behind the library.\n'
			'You\'ll need some \'book smarts\' to get in, hahah!',
			max_dia_cycle=2)

a_albert = NPC(name='ALBERT', title='THE ALCHEMIST',
			dia0='Ah, hello! We don\'t get many visitors here these days. Hmm... are you seeking the treasure?\n'
			'Unfortunately, I will be of no help there. But, if you wish to learn about alchemy ingredients,\n'
			'I\'ll gladly teach you!',
			dia1='Oh, so you ARE interested in learning about alchemy then! Great! So, the most important thing\n'
			'to know is your basic ingredients. First we have WOLFROOT, the most common ingredient used in potion\n'
			'making. This gives your potion susbtance, and helps keep the ingredients mixed thoroughly when punded\n'
			'into a pulp. It won\'t help much with ritual alchemy though. Next we have ground DRAGON TONGUE. Dragons\n'
			'are known for their powerful magic, and even their tongues carry some of their latent magic! When ground\n'
			'up into powder, they impart a huge amount of magical energy to a brew. Great for making potions or spells\n'
			'that need to affect a large area!', 
			dia2='One you should be wary of is powdered AMETHYST. Most alchemists will never touch this, as it\'s only\n'
			'truely useful for performing unsavory magical rituals. Much like the one that binds us to this castle, actually.\n'
			'Opposing that, is powdered DIAMOND. The sheer amount of effort that goes into making it is second only to the\n'
			'incredible effect that it can have - if made correctly, it can be used to bring the dead back to life!',
			dia3='And last but certainly not least, no alchemist should be without his base brew! FELLSHROOM powder,\n'
			'extract of FLAME SLUG, and LIQUID METAL all make for fine bases, though the latter is deathly poisonous,\n'
			'so it\'s only suitable for rituals.', max_dia_cycle=3)

#INVENTORY ITEMS

g_orb = InvItem(name='GREEN CREST ORB', order_slot=1)
g_spoon = InvItem(name='GOLDEN SPOON', order_slot=2)
boar_key = InvItem(name='BOAR KEY', order_slot=3)
broken_sword = InvItem(name='BROKEN SWORD', order_slot=35)
s_needle = InvItem(name='SILVER SEWING NEEDLE', order_slot=4)
w_knife = InvItem(name='WOODEN KNIFE', order_slot=36)
h_book = InvItem(name='ODD BOOK', order_slot=5)
dummy = InvItem(name='dummy', order_slot=9999)


#ENTRANCE HALL

c_entry = InteractObject(name='ENTRANCE',
	description='The entrance to the castle. Though it is open, you do not wish to leave\n'
	'empty-handed.')
a_painting = InteractObject(name='WARLORD PAINTING',
	description='A painting of a tall black-haired warrior, carrying a massive silver sword.\n'
	'The golden frame suggests this is the warlord who once ruled this castle.')
d_statue = InteractObject(name='STATUES',
	description='Several massive statues depicting dragons in various poses. Many have\n'
	'ornate trimmings of silver and gold, and though they have long since been pilfered,\n'
	'the eyes of the statues once clearly were set with gemstones.')
c_crest = BarrierObject(name='CASTLE CREST',
						description='The brilliantly shining castle crest, featuring a golden dragon clutching three\n'
						'orbs. There are red and blue orbs on the crest, but the third slot is missing its orb.',
						control_flag='crest door',
						is_key_lock=True,
						lock_key=g_orb,
						open_desc='The gateway has opened, revealing the stairs to the upper LANDING',
						open_text='You slot the GREEN CREST ORB into the crest, which causes the entire section of\n'
						'wall to lift upwards, revealing a staircase to the upstairs LANDING.',
						cannot_open_desc='Maybe if you find the missing orb, something may happen?',
						zone_to_update=c_entrance,
						zone_new_desc='\nThe stairs to the LANDING on the upper floor are also visible.',
						do_add_exit=True, new_exit=landing)

#DINING ROOM

h_drawer = LootBox(name='DRAWER',
				description='The hidden drawer inside the dining table.',
				item0=boar_key,
				use_desc='You can see something inside the drawer.',
				use_fail_desc='The drawer is empty.')

d_table = BarrierObject(name='DINING TABLE',
		description='This grand dining table once was used to serve massive feasts. It has long\n'
					'since fallen into disuse, and is now covered in a thick layer of dust. Oddly,\n'
					'there is a clean patch of table in the shape of a spoon, as if someone had\n'
					'recently taken it from the table.',
		control_flag='dining table control',
		is_key_lock=True, lock_key=g_spoon, 
		open_desc='The table is now fully set, complete with silverware. The secret compartment is\n'
				  'open.',
		open_text='You place the GOLDEN SPOON on the clean part of the table. As you do, you hear a\n'
				  'dull groan from below you as a small DRAWER pops open from beneath the table.',
		cannot_open_desc='Perhaps if you had a spoon...?',
		zone_to_update=d_hall,
		zone_new_desc='\nAdditionally, you can see the DRAWER that popped out from the dining table.',
		do_add_obj=True, new_obj=h_drawer)

fireplace = BarrierObject(name='FIREPLACE',
						description='A grand fireplace that once lit the dining room. It clearly has not\n'
									'seen use in years, but there are signs of recent movement, like someone\n'
									'or something recently crawled into it.',
						control_flag='fireplace control',
						is_key_lock=True, lock_key=dummy,
						open_desc='Hey! You shouldn\'t see this!',
						open_text='Using your hacker power, you throw the DUMMY into the fireplace,\n'
									'killing the massive spider inside... somehow.',
						not_cross_desc='You decide it would be best not to crawl into the fireplace.',
						is_choice_cross=True,
						choice_prompt='The fireplace is large enough to enter... crawl inside?',
						do_kill_player=True,
						kill_text='As you worm your way into the fireplace, you see a massive shadow\n'
						'descend upon you, followed by the feeling of eight massive, hairy legs gripping\n'
						'you. Suddenly, you feel a sharp pain in your neck, and the world goes blurry as\n'
						'you fade into unconsciousness. The giant spider, which had been living in the\n'
						'abandoned fireplace, drags your corpse back to its nest and slowly devours you.\n'
						'But, hey! It\'s not all bad... your body provided the spider with enough food to\n'
						'survive the winter, so some good came of it still!'
						)


#KITCHEN

b_rack = InteractObject(name='BUTCHER RACK',
	description='Three huge steel racks, once used to prepare beef and other fabulous meats,\n'
	'stained with dried blood from years of use.')

# PANTRY 

pot_sack = InteractObject(name='POTATO SACKS',
	description='Sixteen sacks of potatoes, all of which are empty.')
tom_sack = InteractObject(name='TOMATO SACKS',
	description='Fourteen sacks of tomatoes. All are empty, and one is rather stained, as if\n'
	'the contents were crushed.')
rum_bar = InteractObject(name='RUM BARRELS',
	description='Twenty-one barrels that once contained the highest grade rum. Alas, they\'ve\n'
	'long since been drained.')
odd_box = InteractObject(name='STRANGE BOXES',
	description='Twelve boxes, stained faintly with blood. Each one is big enough for a person\n'
	'to lie down in.')
app_bar = InteractObject(name='APPLE BARRELS',
	description='Six barrels that once held apples. These days, only rotten cores remain.')

#BARRACKS

d_bunk = InteractObject(name='DUSTY BUNK',
	description='Atop this dusty and worn bunk, you find a diary that must have once belonged\n'
				'to a soldier in the castle. Most of the entries are too worn to read, but one\n'
				'remains partially legible:\n\n'
				'    Lord A~&@n dispatched us today, to the nearby village of Unde#@$ot. This is\n'
				'the third month in a row we\'ve raided that poor village. And every time, our\n'
				'lord has had us completely ransack the village for t@~$to@!... It\'s almost\n'
				'absurd, I would say, how much that man loves those... but I cannot raise an\n'
				'objection, lest my head be the next on the chopping block, like poor Siran.')

anton_painting = CodeLock(name='PAINTING', password = '1412',
	description="Behind the paining you discover a vault embedded in the wall.\n"
				"It is locked by a combination lock with 4 dials here, numbered 0 to 9.\n"
				"Set the dials to what number?\n",
	open_desc = 'The vault has already been opened.',
	opening_desc="The vault slowly swings open, revealing a small button. You press it, causing\n"
				"a loud grinding sound which seems to have come from the direction of the kitchen.",
	fail_desc="You set the dials, but nothing happens. Seems that isn't the right combination.",
	zone_to_update=kitchen,new_exit=s_passage,
	new_desc='\nYou can also see an entrance to a HIDDEN PASSAGE here.')

c_bunk = LootBox(name='COLLAPSED BUNK',
				description='You see a bunk for sleeping here. It has long since collapsed due to wood rot.',
				item0=broken_sword,
				use_desc='Something catches your eye beneath the bunk. It takes some effort, but you are\n'
						'able to pull a broken sword out from beneath it. It\'s not much, but it might be\n'
						'worth having a way to defend yourself.',
				use_fail_desc='There\'s nothing else here.')
				
#CELL A

c_door = BarrierObject(name='CELL DOOR',
					description='The door leading to the DUNGEON HALL. It is locked, but oddly, the lock is on\n'
								'the inside of the cell. The lock features a silver engraving of a BOAR.',
					control_flag='boar control', is_key_lock=True,
					lock_key=boar_key,
					open_desc='The door now sits open, allowing access to the DUNGEON CORRIDOR.',
					open_text='You insert the BOAR KEY into the lock and turn it. It takes some effort, but the\n'
							'lock eventually relents, and the door slowly swings open.',
					cannot_open_desc='Unfortunately, it seems that you don\'t have the key to this door.',
					zone_to_update=cell_a, zone_new_desc='\nThe cell door leading to the DUNGEON CORRIDOR is now open.',
					do_add_exit=True, new_exit=dun_hall)

c_bucket = LootBox(name='BUCKET',
				description='An overturned bucket rests on the floor.',
				item0=g_spoon,
				use_desc='You look beneath the bucket and find a GOLDEN SPOON.',
				use_fail_desc='There\'s nothing else beneath the bucket.')

cell_a_bricks = LootBox(name='BRICKS',
				description='Checking the walls, you find some loose bricks, like the Warden mentioned\n'
									'in his journal.',
				item0=s_needle,
				use_desc='Moving the loose brick aside, you notice a SILVER SEWING NEEDLE.',
				use_fail_desc='You check behind the brick again, but find nothing.')

#DUNGEON HALL

d_ornament = InteractObject(name='DRAGON ORNAMENTS',
	description='Several glimmering dragon ornaments line the halls of the dungeon. Even in\n'
				'the darkness, they glimmer with a faint, eerie light.')

c_door_d = InteractObject(name='RUSTED CELL',
	description='A rusted over cell door. It seems to have not been used in many years. You\n'
				'carefully try to open it, but it does not move even an inch. In the cell, \n'
				'you can see the remains of a skeleton.')

c_door_e = InteractObject(name='RUINED DOOR',
	description='You see the remains of a cell here. The ceiling of the cell has long since\n'
				'collapsed, and the cell door is buckled nearly in half from the impact.')

#CELL B

cell_b_bricks = LootBox(name='BRICKS',
				description='Running your hand along the wall, you notice a loose brick, like\n'
							'the Warden\'s journal mentioned.',
				item0=w_knife,
				use_desc='Moving the brick aside, you find a WOODEN KNIFE. Seems one of the\n'
						'prisoners had made a shiv of some sort. Deciding that you might want\n'
						'some kind of weapon, you take it with you.',
				use_fail_desc='You check behind the brick again, but find nothing else.')

cell_b_journal = InteractObject(name='FADED JOURNAL',
	description='A faded and worn journal kept by the cell\'s past occupant. Most of the\n'
				'pages are too worn to read, but one entry remains intact:\n\n'
				'    14 Bluestar, 13#&\n\n'
				'That blasted oaf! I had almost done it! I was so close to the treasure...\n'
				'but then that blasted librarian felt the need to take a midnight stroll and\n'
				'found me! I will surely spend the rest of my days and moreso beyond rotting\n'
				'away in this cell... but perhaps, if another were to find this journal, they\n'
				'can exact my revenge and clain the treasure. If you\'re reading this, know\n'
				'that the treasure is guarded by a devilish mathematical puzzle, surely meant\n'
				'to keep the uneducated masses away. The orbs are key, each i-\n\n'
				'The journal entry suddenly ends here. A faint bloodstain covers the bottom\n'
				'of the page.')

#CELL C

cell_c_bricks = InteractObject(name='BRICKS',
	description='Upon closer inspection of the far wall of the cell, you find a loose\n'
				'brick. Moving it aside, you find nothing but some cobwebs.')

footprints = InteractObject(name='FOOTPRINTS',
	description='On the floor of the cell, you can see footprints in the dust, as if\n'
				'someone has been moving in and out of this cell recently.')
cell_bunk = InteractObject(name='BUNK',
	description='This bunk is completely free of dust, and seems to have been used\n'
				'just recently.')

#WARDEN'S OFFICE

w_diary = InteractObject(name='RED DIARY',
	description='This diary must have belonged to the dungeon\'s warden. It is still\n'
				'in good condition, and most of the entries are legible. Poring through\n'
				'its pages, one entry in particular stands out:\n\n'
				'    23 Duskmoon, 13#%\n\n'
				'Today, while making my usual rounds of the dungeon, I caught one of those\n'
				'filthy maggots hiding something behind a loose brick in the wall. This, of\n'
				'course, pissed me off something fierce, even more so when I realized the little\n'
				'worm was hiding contraband behind it! Food, even! Hah, as if these fools are\n'
				'allowed to eat... Naturally, he got sent out to be... \'processed\'. But, I will\n'
				'admit, he gave me an idea. I can hide my own secret treasure behind a loose brick\n'
				'to keep it from prying eyes... I\'ll have to do a sweep of the prison tomorrow,\n'
				'check for any more loose BRICKS.')

gold_chest = LootBox(name='GOLDEN CHEST',
					description='It\'s an ornate golden chest, not particularly large, but enough to hold a\n'
								'small valuable item.',
					item0=g_orb,
					use_desc='You open the chest, and find a glittering orb of emerald, similar to the orbs\n'
							'set in the castle crest in the entrance hall.',
					use_fail_desc='You check the chest again, but all you find is a small spider that has taken up\n'
									'residence in the empty space.')


w_bricks = BarrierObject(name='BRICKS',
			description='You check along the walls and find the brick mentioned in the Warden\'s\n'
						'journal. Moving the brick aside, you notice a small button.',
			control_flag='brick control',
			open_desc='You check behind the brick again, but shockingly, the button you pressed\n'
			'is still pressed.',
			open_text='As you press the button, you hear the sound of sliding stone. Looking to\n'
					'the side, you see a secret panel in the wall has slid open, revealing a\n'
					'GOLDEN CHEST.',
			cannot_open_desc='You decide that pressing strange buttons is a bad idea.',
			is_choice_cross=True, choice_prompt='Push the button?',
			zone_to_update=ward_offc, zone_new_desc='\nA GOLDEN CHEST is visible in the revealed hidden chamber.',
			do_add_obj=True, new_obj=gold_chest)

#LANDING

paintings = InteractObject(name='PAINTINGS',
	description='A collection of paintings hangs above the staircase. In many of them, a warrior\n'
				'with jet-black hair is depicted gesturing victoriously over a battlefield. There\n'
				'is also a painting of the same warrier riding a brilliant golden dragon, with three\n'
				'colored gemstones set in its forehead.')

s_window = InteractObject(name='WINDOW',
	description='A brilliant stained glass window rests within the south wall of the landing. It\n'
				'depicts a black-haired warrior posin regally with a glittering sword of silver.')

#AUDIENCE HALL

g_throne = InteractObject(name='THRONE',
	description='The brilliant golden throne that Lord Anton once reigned from. Even decades after\n'
				'the castle\'s fall, it still glimmers as brightly as the day it was created. You\n'
				'decide to take a seat for a brief moment to rest your weary legs, but you cannot\n'
				'help but to belt out a haughty laugh from atop the throne. \"Oi! Stop that, you\n'
				'fool! I may be dead, but that is still MY throne!\", Anton shouts at you angrily.\n'
				'You decide that it would be best to not disturb him further, even in death, so you\n'
				'get up from the throne and carry on.')
c_banners = InteractObject(name='BANNERS',
	description='Brilliant crimson banners hang from the pillars of the audience hall, all bearing\n'
				'the castle\'s golden dragon motif.')

#LIBRARY

hist_book = InteractObject(name='HISTORY BOOK',
	description='This book lies open on the table, as if the reader was suddenly interrupted. It\n'
				'details the various villages and cities in the region, and their primary exports.\n'
				'Seems like this book was used to plan out the castle\'s raids on nearby settlements.\n')
s_bookshelf = BarrierObject(name='BOOKSHELF',
							description='It\'s a massive bookshelf, filled with many rows of books. One shelf is missing a book.',
							control_flag='vault control',is_key_lock=True,lock_key=h_book,
							open_desc='The bookshelf has moved aside, revealing the way to the VAULT.',
							open_text='You notice that the odd book from the study would fit perfectly into the empty\n'
										'spot. Upon placing it on the shelf, you hear a loud grinding noise as the\n'
										'entire shelf slides aside, revealing a secret passageway... perhaps this is\n'
										'the path to the VAULT?',
							cannot_open_desc='Perhaps if you had a book that would fit on the shelf...',
							zone_to_update=library,do_add_exit=True,new_exit=vault,
							zone_new_desc='\nYou can also see a passage leading to the VAULT here.')
chandelier = InteractObject(name='CHANDELIER',
	description='This brilliant crystal chandelier once provided light to the library. It seems that\n'
				'after decades of disrepair, the ceiling holding it finally gave way, sending it\n'
				'crashing to the ground. Chunks of shattered wood from the support beam it once hung\n'
				'from litter the ground around it.')
gems_book = InteractObject(name='GEM BOOK',
	description='This book details the value of various gemstones that can be found in the local area.\n'
				'Notably, one page in particular is worn, as if it was frequently referenced:\n\n'
				'    \"Of course, the most common gemstones that can be found in the #~@&*@ region are\n'
				'also frequently used in magical contraptions. This oftentimes causes them to be traded\n'
				'at a high price, despite their relative abundance in the region.\n\n'
				'    The first is the RUBY, associated with the element of Fire and the emotions of Wrath\n'
				'and Loss. Many artificers will pay as high as twenty gold pieces for a quality ruby. Next,\n'
				'we have the EMERALD, associated with the element of Wind and the emotions of Joy and\n'
				'Fulfillment. The emerald is an excellent tool for the creation of magical locks, and as\n'
				'such, the ambitious locksmith can expect to pay as much as twenty-five gold pieces for one.\n'
				'Third, we have the relatively unusual AMETHYST, associated with the element of Darkness\n'
				'and the emotions of Despair and Greed. The ametyhyst is often only used in its powdered\n'
				'form, and is commonly used in rituals pertaining to curses. Given this distasteful use,\n'
				'it commonly sells for as little as thirty gold pieces, despite being rather scarce.\n\n'
				'    Additionally, there are several gemstones that despite having no practical use, are\n'
				'nontheless valued for their beauty. Chief among these is the SAPPHIRE. Despite being quite\n'
				'common and having no magical use to speak of, one can expect a single sapphire to cost as\n'
				'much as ten gold pieces. And, of course, we cannot forget that symbol of wealth, the BISMUTH.\n'
				'This unusual stone is exceptionally rare, but the wealthy have been known to pay as much as\n'
				'two hundered gold pieces to acquire one! The miner who finds one is a lucky man, indeed.\"')
c_book = InteractObject(name="CASTLE HISTORY",
	description="A book detailing the history of Castle Dawnstar. It would seem the castle was built over\n"
				"two hundred years ago, though its final owner only claimed it one hundred years ago to\n"
				"this very day.")

#STUDY

w_desk = InteractObject(name='DESK',
	description='This desk must have once belonged to the lord of the castle. Atop it rests a diary detailing\n'
				'the lord\'s rise to power. One excerpt in particular catches your eye:\n\n'
				'    \"I was right to raid that sorceror\'s den! The bastards were using black\n'
				'magic to create magical abominations in an attempt to defeat me! The half-snake,\n'
				'half-falcon beast they sent after me nearly did me in, even, if it were not for\n'
				'my trusty silver dagger. It would seem that the beasts are invulnerable to all\n'
				'weapons save for those made of silver... I claimed their research journals, and now\n'
				'I\'ve set my alchemists about creating a creature of my own to guard my treasure...\n'
				'The chances of anyone finding a weapon made of silver in this area are close to none,\n'
				'given that I personally captured every silver mine around to forge my arms.\"')
m_lamp = InteractObject(name='LANTERN',
	description='A strange silver lantern rests upon the desk. Despite this place being abandoned for years, \n'
				'it still glows with a dull green flame, bathing the room in its gentle light.')
k_book = LootBox(name="ODD BOOKSHELF",
				description="One of several ornate bookshelves adorning the study.",
				item0=h_book,
				use_desc="While examining this bookshelf, you notice an odd book that seems to have no\n"
						"pages. It seems rather odd that someone would keep such an object around, so you\n"
						"take it with you.",
				use_fail_desc="You scour the bookshelf for anything else of use, but find nothing.") 

#THE VAULT

dragon_altar = DragonAltar()

chimera = BarrierObject(name='CHIMERA',
						description='Sleeping in the center of the room rests a massive chimera. It seems to have\n'
									'been made by stitching together many monster parts, including the wings of a\n'
									'drake, the head of a serpent, the body of a grizzly bear, the claws of a dire\n'
									'crab, and the tail of a shark. The creature is sleeping soundly in the hallway.',
						control_flag='chimera life',
						is_key_lock=True, lock_key=s_needle,
						open_desc='The chimera lies on the floor, dead. You\'re surprised that something as simple\n'
									'as a silver sewing needle was able to kill such an abomination.',
						open_text='Recalling what you had learned about the beast\'s weakness, you carefully approach\n'
									'it, silver needle in hand. Just as you get close, it wakes up and unleashes an angry\n'
									'hiss, but before it can strike, you stab into its bear-like body with the needle. The\n'
									'creature hisses as it begins to flail widly, its body slowly seeming to deflate, before\n'
									'finally collapsing into a heap on the floor. With the beast defeated, you are free to\n'
									'approach the DRAGON ALTAR.',
						is_choice_cross=True, choice_prompt='Attempt to sneak past the chinera?',
						not_cross_desc='You decide not to risk waking the sleeping beast.',
						do_kill_player=True,
						kill_text='You very cautiously sneak across the wall past the chimera. You had just managed to get\n'
									'past it, when you hear a quiet hiss. Looking back, you see the beast rising to a standing\n'
									'position, raising its claws angrily. Before you can even motion to flee, the beast is upon\n'
									'you, gripping you tightly in its massive, meaty claw. You flail around in a panic, trying to\n'
									'escape, but to no avail. The last thing you see before you die is the snake head rearing back\n'
									'to bite off your head.\n\n'
									'But, hey! Guess what? You\'re the lucky fiftieth adventurer to die to the chimera! Here is your\n'
									'prize!\n\n'
									'Recieved a CONSOLATION PRIZE.',
						zone_to_update=vault, zone_new_desc='\n\nThe path is clear. The DRAGON ALTAR awaits.',
						do_add_obj=True, new_obj=dragon_altar)

#ALCHEMY LAB

al_notes = InteractObject(name='NOTES',
	description='These notes seem to have been written by the castle alchemist. They seem to describe how to\n'
				'reverse a spell of soul binding, though a splatter of blood obscures most of the instructions.\n'
				'The small amount that is legible reads:\n\n'
				'    \"Though the counter-ritual is very safe to perform, it is very sensitive to the ingredients\n'
				'used. If all the ingredients are added correctly, heating the cauldron will create a puff of green\n'
				'smoke. Any other color indicates a misstep on the ritualist\'s part.\"')
cauldron = AlchemyPot()
ing_shelf = InteractObject(name='STORAGE',
	description='Rows upon rows of shelving, containing a wide variety of alchemy ingredients. Most of the ingredients\n'
				'are still in stock, including rarities such as powdered amethyst, ground dragon tongue, and root of\n'
				'deathbloom.')

c_entrance.update_atts(exit0=d_hall, exit1=barracks, exit2 = landing, npc0=v_hartz,
	obj0=c_entry, obj1=a_painting, obj2=d_statue, obj3=c_crest)
d_hall.update_atts(exit0=c_entrance, exit1=kitchen, obj0=h_drawer,
		obj1=d_table, obj2=fireplace)
kitchen.update_atts(exit0=d_hall,exit1=pantry,npc0=c_canna,
	npc2=c_abello, obj0=b_rack)
pantry.update_atts(exit0=kitchen,obj0=pot_sack,obj1=tom_sack,
	obj2=rum_bar,obj3=odd_box,obj4=app_bar)
barracks.update_atts(exit0=c_entrance,npc0=s_loton,obj0=d_bunk,
	obj1=anton_painting,obj2=c_bunk)
s_passage.update_atts(exit0=kitchen, exit1=cell_a)
cell_a.update_atts(exit0=s_passage,obj0=c_bucket,obj1=c_door,
	obj2=cell_a_bricks)
dun_hall.update_atts(exit0=cell_a,exit1=cell_b,exit2=cell_c,
	exit3=ward_offc,obj0=d_ornament,obj1=c_door_d,obj2=c_door_e)
cell_b.update_atts(exit0=dun_hall,obj0=cell_b_bricks,obj1=cell_b_journal)
cell_c.update_atts(exit0=dun_hall,obj0=cell_c_bricks,obj1=footprints,
	obj2=cell_bunk)
ward_offc.update_atts(exit0=dun_hall,obj0=w_diary,obj1=w_bricks)
landing.update_atts(exit0=aud_hall,exit1=library,exit2=a_lab,
	exit3=c_entrance,obj0=paintings,obj1=s_window)
aud_hall.update_atts(exit0=landing,npc0=a_anton,obj0=g_throne,
	obj1=c_banners)
library.update_atts(exit0=landing,exit1=study,obj0=hist_book,
	obj1=s_bookshelf,obj2=chandelier,obj3=gems_book,obj4=c_book)
study.update_atts(exit0=library,npc0=a_albert,obj0=w_desk,
	obj1=m_lamp,obj2=k_book)
vault.update_atts(exit0=library,obj0=chimera)
a_lab.update_atts(exit0=landing, obj0=al_notes,obj1=cauldron,
	obj2=ing_shelf)	


def command_parse():
	command = None
	player_in_filtered = []
	global area_shown
	global swear_jar
	global current_zone
	r = 0
	accepted_commands = ['MOVE', 'GO', 'WALK', 	 #index 0-2 = 'move' commands
	'TALK', 'SPEAK', 							 #index 3-4 = 'talk' commands
	'LOOK',										 #index 5 = 'look around' command
	'USE', 'CHECK','OPEN',						 #index 6-8 = 'use' an object
	'INVENTORY', 'ITEM', 'ITEMS', 'BAG',		 #index 9-12 = open inventory
	'QUIT', 'EXIT',								 #index 13-14 = quit game
	'HELP', '?',								 #index 15-16 = help command
	'WAIT',] 									 #index -1 = 'wait' command]
	banned_words = ['CRAB', 'CALCULUS', 'LIGHTNING', 'CAW']#banned words
	mouth_soap = [f"Well exc"+"u"*3000+"se me, Princess!",
	"Keep talkin' like that, see where it gets ya.",
	"<InputError: User unintelligible!>",
	"Same to you, bub!",
	"Yeah, real smart, wiseguy.",
	"Try some nice soap for dinner tonight.",
	"Look at me, I\'m the big bad player, swearing at an innocent text parser!",
	"Que?",
	"Maybe try that again but a little bit nicer?"]
	smartypants = [
	"KILL", "HARM", "VIOLENCE", "MURDER", "STAB", "HIT", "PUNCH", "HURT",
	"EAT",
	"FLY", "DRIVE", "SWIM", "DRILL", "PICK", "HACK", "CHEAT",
	"DIE", "KEEL OVER", "PERISH", "GIVE UP"
	]
	non_violent = [
	"You should really curb those violent tendancies!",
	"Violence is not the answer!",
	"And what on earth would THAT accomplish, hmm?",
	"You and what army?"
	]
	not_hungry = "You aren\'t hungry."
	cant_do = [
	"You wish!",
	"You can\'t do that!",
	"And how do you expect to do that?",
	"You wot, mate?" 
	]
	no_die = [
	"But you have so much to live for!",
	"I don\'t think dying will help you find the treasure...",
	"You punch yourself. It hurts. Are you strong, or weak?",
	"Unfortunately it seems you are still alive."
	]
	help_text = (f"\nAccepted commands:\n\n"
	f"MOVE/GO/WALK <location>: Move to the specified location.\n\n"
	f"TALK/SPEAK <character>: Talk to the specified character. \n\n"
	f"USE/CHECK/OPEN <object>: Use or check the specified object.\n\n"
	f"INVENTORY/ITEM/BAG: Look at the items you're carrying.\n\n"
	f"LOOK: Look around at the area you're in. Useful if you don't remember\n"
	f"what's in the area.\n\n"
	f"WAIT: Do nothing and pass time.\n\n"
	f"HELP/?: Opens this information. \n\n"
	f"QUIT/EXIT: Exits the game. You'll lose all progress, so be careful!\n\n"
	f"You don't need to type in all caps to give commands in this game, nor\n"
	f"do you have to speak like a caveman - \"Talk to Bob\" is perfectly fine.\n\n")	
	while not command: 
		print(f"\nWhat will you do? (type 'help' for help)\n")
		player_in = input().upper().split()
		if not [word for word in player_in if word in banned_words] and not [word for word in player_in if word in smartypants]:
			if not [word for word in player_in if word in accepted_commands]:
				print(f"\nI don't understand. Please use verb commands like"
				f" 'Go to the castle' or 'Talk to Bob'\n")
				player_in = ''
			else:
				player_in_filtered.clear()
				if [word for word in player_in if word in accepted_commands[0:3]]: #movement command
					player_in_filtered.append(' '.join([word for word in player_in if word not in accepted_commands and word in ' '.join(current_zone.all_exit_names)]))
					if not [word for word in player_in_filtered if word in current_zone.all_exit_names]:
						print(f"\nI don't understand. Please say where you"
						f" wish to move i.e. 'Move to the house'\n")
						player_in = ''
					else:
						player_in_filtered.append(' '.join([word for word in player_in_filtered if word in current_zone.all_exit_names]))
						targ_zone = ' '.join([word for word in current_zone.all_exit_names if word in player_in_filtered])
						go_zone = current_zone.all_exits[current_zone.all_exit_names.index(targ_zone)]
						current_zone = go_zone
						c_zone = go_zone
						area_shown = False
						command='move'

				elif  [word for word in player_in if word in accepted_commands[3:5]]: #talk command
					player_in_filtered.append(' '.join([word for word in player_in if word not in accepted_commands and word in ' '.join(current_zone.all_npcs_name)]))
					if not [word for word in player_in_filtered if word in current_zone.all_npcs_name]:
						print(f"\nI don't understand. Please say who you"
						f" wish to talk to i.e. 'Speak to Bob'.\n")
						player_in = ''
					else:
						targ_npc = ' '.join([word for word in current_zone.all_npcs_name if word in player_in_filtered])
						targ_npc=current_zone.all_npcs[current_zone.all_npcs_name.index(targ_npc)]
						if targ_npc.current_dia > targ_npc.max_dia_cycle:
							targ_npc.current_dia = 0
						if targ_npc.current_dia == 3:
							print(f"\n{targ_npc.dia3}\n")
						elif targ_npc.current_dia == 2:
							print(f"{targ_npc.dia2}\n")
						elif targ_npc.current_dia == 1:
							print(f"{targ_npc.dia1}\n")
						elif targ_npc.current_dia == 0:
							print(f"{targ_npc.dia0}\n")
						targ_npc.current_dia += 1
						command='talk'


				elif [word for word in player_in if word in accepted_commands[5]]: #look command
					player_in_filtered.append(' '.join([word for word in player_in if word not in accepted_commands]))
					print(f"\n{current_zone.look_desc}\n")
					command = 'look'

				elif [word for word in player_in if word in accepted_commands[6:9]]: #use command
					player_in_filtered.append(' '.join([word for word in player_in if word not in accepted_commands and word in ' '.join(current_zone.all_objs_name)]))
					if not [word for word in player_in_filtered if word in current_zone.all_objs_name]:
						print(f"I don't understand. Please say what you"
						f" wish to interact with i.e. 'Use chest'.\n")
						player_in = ''
					else:
						use_target = current_zone.all_objs[current_zone.all_objs_name.index(' '.join(player_in_filtered))]
						if type(use_target) == LootBox:
							use_target.chest()
						elif type(use_target) == SwitchObject:
							use_target.switch_use()
						elif type(use_target) == BarrierObject:
							use_target.barrier_open()
						elif type(use_target) == DragonAltar:
							use_target.d_altar()
						elif type(use_target) == AlchemyPot:
							use_target.alch_puzzle()
						elif type(use_target) == CodeLock:
							use_target.code_lock()
						else:
							print(use_target.description)

						command = 'use'	

				elif [word for word in player_in if word in accepted_commands[9:13]]: #inventory command
					if player.inventory:
						show_inventory()
					else:
						print("You don't have anything!")
					command = 'inventory'

				elif  [word for word in player_in if word in accepted_commands[13:15]]:
					if input(f"Are you sure you want to quit? Yes/No:\n").upper() == 'YES':
						player.quit = True
						command = 'exit'

				elif  [word for word in player_in if word in accepted_commands[15:17]]:
					print(help_text)
					command='help'

				elif [word for word in player_in if word in accepted_commands[-1]]: #wait command
					# player_in_filtered.clear()
					player_in_filtered.append(' '.join([word for word in player_in if word not in accepted_commands])) #wait command
					command = 'wait'


		else:
			if [word for word in player_in if word in banned_words]:
				print(choice(mouth_soap))
				swear_jar +=1
				if swear_jar == 5:
					print(f"\nNo, really, keep this up and you'll have a bad time.\n")
			else:
				if [word for word in player_in if word in ["KILL", "HARM", "VIOLENCE", "MURDER", "STAB", "HIT", "PUNCH", "HURT"]]:
					print(choice(non_violent))
				elif [word for word in player_in if word in ["EAT"]]:
					print(not_hungry)
				elif [word for word in player_in if word in ["FLY", "DRIVE", "SWIM", "DRILL", "PICK", "HACK", "CHEAT"]]:
					print(choice(cant_do))
				elif [word for word in player_in if word in ["DIE", "KEEL OVER", "PERISH", "GIVE UP"]]:
					print(choice(no_die))
				else:
					print("I don\'t know what it is, but something you just said really shorts my circuits!")
			command = 'bad player'

	return None 

def title_menu():
	global new_game
	player_in = ''
	while not player_in:
		player_in = input("Welcome to Treasure of Castle Dawnstar!\n"
						"Type START to begin the game, or QUIT to quit.\n\n").upper()
		if "START" in player_in:
			return None
		elif "QUIT" in player_in:
			player.quit = True
		else:
			print("I don\'t understand. Please type either START or QUIT.")
			player_in = ''

while not player.quit:
	title_menu()
	# import pdb; pdb.set_trace()
	if new_game and not player.quit:
		game_intro()
		current_zone = c_entrance
		c_zone = c_entrance
		player.inventory = []
	while swear_jar <10 and player.is_dead==False and player.quit==False and not game_complete and not alchemy_secret:
		room_info()
		command_parse()

	if swear_jar >= 10:
		print(f"\n\n\nCome back when you've washed your mouth out, kid.\n\n\n"
			"GAME OVER")
	elif player.is_dead:
		print("You have died. Game Over.")
	elif game_complete:
		input("\n\nAs you enter the passageway behind the Dragon Altar, all goes dark for a moment.\n"
			"Feeling your way along the narrow passage, you press on and eventually a glimmer of\n"
			"light catches your eye. As you draw near, magical torches around the room respond to\n"
			"your presence, revealing the true treasure of Castle Dawnstar... The Gilded Dragon\n"
			"Blade, a grand two handed sword with gold inlay along the blade, depicting a \n"
			"grand dragon ascending into the sky, surrounded by three glowing orbs of red\n"
			"blue, and green. Additonally, you can see the grand Armor of Wealth, a suit of\n"
			"armor forged entirely from the incredibly rare Bismuth. Though it makes for poor\n"
			"battle gear, the armor was supposedly forged as a testament to warlord Anton\'s might.\n"
			"Surprisingly, the armor is surprisingly light, undoubtedly some form of magical\n"
			"enchantment to make it easier to wear. In the far corner of the room, you also find\n"
			"a modest stockpile of various highly valuable gemstones, which will surely sell for a mint.\n"
			"Donning the armor, and slinging the blade and haul of gems over your shoulder, you begin\n"
			"your exit from the castle.")
	if alchemy_puzz_done:
		input("As you make your way down the stairs to the entrance hall, you are surprised\n"
			"to see the denizens of the castle awaiting you along the room. As you pass by,\n"
			"each of the castle\'s servants bows in deep gratitude towards your actions.\n"
			"As you approach the exit to the castle, the spectre of warlord Anton approaches\n"
			"you. Silently, he places his ghostly hand on your shoulder and simply nods while\n"
			"looking you in the eye. Despite his ethereal form, you can almost feel the weight\n"
			"of his once powerful arm, before it gently disappates into the air as Anton\'s\n"
			"spirit moves on to the afterlife.\n\n\n")
		input("Congratulations! You have discovered the true treasure of Castle Dawnstar!\n"
			"However! This is only one of three endings! Can you find all three?\n\n\n\n\n\n\n"
			"ENDING 1 OF 3: The Sacred Treasure\n"
			"FIN.")
	elif alchemy_secret:
		input("Tne strange smoke seems to expand, rapidly filling the room, so dense that\n"
			"you feel almost as if you're swimming through it. Slowly, it begins to settle\n"
			"down at floor level, coating the floor in a thick fog. Suddenly, you hear a\n"
			"loud man\'s laugh from outside.\n\n")
		input("No sooner do you step out of the alchemy lab do you see warlord Anton,\n"
			"somehow brought back to life. He looks you in the eye, a confident grin\n"
			"on his face. \"Well then! I really didn\'t expect you to find a way to\n"
			"bring us all back to life! The treasure is yours, friend, as promised,\n"
			"but now I can offer you something even more valuable... a seat of power\n"
			"as I reclaim what is rightfully mine!\" \n\n")
		input("After careful consideration, you accept Anton on his offer. Over the\n"
			"following decade, you command his ever growing army as it expands and\n"
			"subjugates the surrounding lands into the reborn Dawnstar Kingdom.\n"
			"Though, oddly, it seems as though being trapped in his castle for\n"
			"a hundred years made Anton go soft. His methods of warmongering are\n"
			"nowhere near as ruthless as in his past days, nor does he mercilessly\n"
			"rob his territories for supplies. Indeed, the citizens of the kingdom\n"
			"thrive and flourish under the protection of the legendary warlord, and\n"
			"it seems the land is heading towards a new era of enlightenment...\n"
			"...but, only time will tell.\n\n\n\n\n")
		input("Congratulations! You\'ve discovered the secret ending and brought the\n"
			"New Age of Dawnstar into existence!\n\n\n\n\n\n\n"
			"ENDING 3 OF 3: Rebirth of the Dawnstar Kingdom\n"
			"FIN")
	elif game_complete and not alchemy_puzz_done:
		input("As you make your way out of the castle, you suddenly get a very bad feeling in\n"
			"your stomach, as the armor you claimed suddenly increases in weight greatly. You\n"
			"manage to still find your way back to town, however no matter who you ask, noone\n"
			"will buy the blade or armor from you, claiming them to be obvious fakes. You\n"
			"do manage to sell the gemstones, making enough money to live out the rest of\n"
			"your days in relative luxury, but no matter what you try, you cannot rid yourself\n"
			"of the sword nor the armor. They somehow always manage to reappear among your\n"
			"personal possessions, almost as if they are following you.\n\n\n")
		input("Congratulations! You were able to uncover the treasure of Castle Dawnstar,\n"
			"but at what cost...?\n\n\n\n\n\n\n"
			"ENDING 2 OF 3: Cursed Treasure\n"
			"FIN")
	if not player.quit:	
		if input("\n\nWould you like to play again? Yes/No:\n").upper() == "YES":
			swear_jar = 0
			game_complete = False
			alchemy_puzz_done = False 
			alchemy_secret = False
			player.is_dead = False
			current_zone = c_entrance
			player.inventory = []
			player.flag0 = False
			player.d_table_open = False
			player.fireplace = False
			player.boar_door = False
			player.warden_brick = False
			player.chimera_flag = False
			player.vault_open = False
			player.c_crest_open=False
			c_entrance.update_atts(exit0=d_hall, exit1=barracks, npc0=v_hartz,
			obj0=c_entry, obj1=a_painting, obj2=d_statue, obj3=c_crest)
			d_hall.update_atts(exit0=c_entrance, exit1=kitchen, obj0=h_drawer,
			obj1=d_table, obj2=fireplace)
			kitchen.update_atts(exit0=d_hall,exit1=pantry,npc0=c_canna,
			npc2=c_abello, obj0=b_rack)
			barracks.update_atts(exit0=c_entrance,npc0=s_loton,obj0=d_bunk,
			obj1=anton_painting,obj2=c_bunk)
			cell_a.update_atts(exit0=s_passage,obj0=c_bucket,obj1=c_door,
			obj2=cell_a_bricks)
			cell_b.update_atts(exit0=dun_hall,obj0=cell_b_bricks,obj1=cell_b_journal)
			ward_offc.update_atts(exit0=dun_hall,obj0=w_diary,obj1=w_bricks)
			library.update_atts(exit0=landing,exit1=study,obj0=hist_book,
			obj1=s_bookshelf,obj2=chandelier,obj3=gems_book,obj4=c_book)
			study.update_atts(exit0=library,npc0=a_albert,obj0=w_desk,
			obj1=m_lamp,obj2=k_book)
			vault.update_atts(exit0=library,obj0=chimera)
			a_lab.update_atts(exit0=landing, obj0=al_notes,obj1=cauldron,
			obj2=ing_shelf)
			h_drawer.was_opened = False 
			c_bunk.was_opened = False
			c_bucket.was_opened = False
			cell_a_bricks.was_opened = False
			cell_b_bricks.was_opened = False 
			gold_chest.was_opened = False
			k_book.was_opened = False
			anton_painting.locked=True
		else:
			print("\nThank you for playing!")
			player.quit = True