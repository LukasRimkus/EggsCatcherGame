# The purpose of the game is to catch as many eggs as possible using a 
# brown box which is cotrolled (default) using arrow keys to left and right.
# All the keyboard controls are saved in the list 'controls' and 
# in the 'keyboard_buttons.txt' file
# The pause can be turned on by default when you press the 'Escape' keyboard button.
# Also, there is included a 'boss key' which can be activated using the 'b' 
# keyboard button (default).
# All the buttons can be changed in the game 'settings' menu.
# There are three different keyboard combinations for cheats: 
# 1) if you type in 'life', you receive an extra life
# 2) if you type in 'slow', you slow a game a bit (at the beginning of the 
# game the effect can be hardly noticeable; you can type in the code
# several times to get a stronger effect on the pace of the game)
# 3) 'Control_L+Shift_L+c' decrease the lives by one
# As you progress, the game becomes more difficult. But per 20 new points 
# you receive an extra life. 
# The best five players are included in the leaderboard, the results are 
# saved in the 'leaderboards.txt'file.
# You can turn off the game even if you have not finished playing, as the 
# game state is saved in the 'save_game_state.txt' file
# In some computers the pace of game can be very slow or vice versa (tested that),
# in this case you would need to edit the value of the 'coefficient_of_falling' in 
# the line 734 which determines the velocity of falling eggs.
# Standard screen size is 1536x864.


from random import randint
from tkinter import Tk, Entry, PhotoImage, Button, messagebox, Canvas
from time import sleep


def configure_window():
    global width, height
    width, height = 1536, 864
    ws = window.winfo_screenwidth()  # computers screen size
    hs = window.winfo_screenheight()
    x = (ws/2) - (width/2)  # calculate center
    y = (hs/2) - (height/2)
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))  # window size
    window.resizable(False, False)
    window.title("Eggs Collection Simulator")

 
def getting_control_buttons():
    buttons_file = open('Data/keyboard_buttons.txt', 'r')
    text = buttons_file.readlines()

    # if empty
    if not text:
        messagebox.showwarning(title='Error!', message='Error in the keyboard buttons file... There should be the names of 4 buttons...')
        quit()
    else:
        # 4 keyboard buttons
        for i in range(4):
            controls[i] = text[i].rstrip()
     
    buttons_file.close()


# update keyboard buttons when they are changed by a player
def updating_control_buttons():
    buttons_file = open('Data/keyboard_buttons.txt', 'w')

    # 4 keyboard buttons
    for i in range(4):
        buttons_file.write(controls[i])
        buttons_file.write('\n')
 
    buttons_file.close()


def ask_for_name_first_time():
    global get_name, settings, error_invalid_name, ask_my_name_canvas, just_turned_on_the_game

    # signifies that the settings screen is off
    settings = False
    just_turned_on_the_game = True

    ask_my_name_canvas = Canvas(window, width=1536, height=864)
    ask_my_name_canvas.pack(fill="both", expand=True)

    ask_my_name_canvas.create_image(0, 0, image=bg5, anchor='nw')

    ask_my_name_canvas.create_text(768, 100, text="HI! Please type in your name!",
                                   fill='black', font=("Arial Bold", 40))

    get_name = Entry(window, font=("Arial Bold", 25), bg='#c5f6f6')
    ask_my_name_canvas.create_window(557, 250, anchor='nw', window=get_name)

    begin = Button(window, text='Start the adventure!', bg='#c5f6f6',
                   activebackground='#3D16DB', fg='black', font=("Arial Bold", 30), command=get_the_name)
    ask_my_name_canvas.create_window(550, 350, anchor='nw', window=begin)


def ask_for_name_again():
    global settings
    get_name.delete(0, 'end')

    # if the current screen is not settings one
    if not settings:
        ask_my_name_canvas.create_text(768, 600,
            text="Please enter a valid name! \nOnly alpha characters and numeric values are valid!" +
            "\nThe maximum number of characters is 12", fill='black', justify='center', font=("Arial Bold", 40))
    else:
        change_name_canvas.create_text(768, 500,
            text="Please enter a valid name!\nOnly alpha characters and numeric values are valid!" +
            "\nThe maximum number of characters is 12", fill='black', justify='center', font=("Arial Bold", 40))


# taking the name from the entry box
def get_the_name():
    global name, settings, old_name

    name = get_name.get()
    name = name.strip()

    get_name.delete(0, 'end')
    if (len(name) == 0 or not name.isalnum() or len(name) > 12):
        if settings:
            name = old_name

        ask_for_name_again()
    else:
        menu_contents()


# creating the menu screen and displaying the menu buttons
def menu_contents():
    global state_of_the_last_game, resume, settings, menu_is_on

    settings = False
    menu_is_on = True
    # destroying the previous screen
    destroy_menu_items(window)

    main_menu_canvas = Canvas(window, width=width, height=height)
    main_menu_canvas.pack(fill="both", expand=True)

    main_menu_canvas.create_image(0, 0, image=bg3, anchor='nw')

    main_menu_canvas.create_text(760, 65, text="Hello, " + name + "!", justify='center',
								fill='black', font=("Arial Bold", 40))

    resume = Button(window, text="Resume", state='disabled', command=resume_button_pressed,
					bg='#c5f6f6', activebackground='#3D16DB', fg='black', font=("Arial Bold", 35), bd=0)
    main_menu_canvas.create_window(650, 140, anchor='nw', window=resume)

    start_the_game = Button(window, text="Start", bg='#c5f6f6', activebackground='#3D16DB',
							fg='black', command=start, font=("Arial Bold", 35))
    main_menu_canvas.create_window(650, 240, anchor='nw', window=start_the_game)

    leaderboards = Button(window, text="Leaderboards", bg='#c5f6f6', activebackground='#3D16DB',
						  fg='black', font=("Arial Bold", 35), command=show_leaderboards)
    main_menu_canvas.create_window(650, 340, anchor='nw', window=leaderboards)

    how_to_play = Button(window, text="How to play", bg='#c5f6f6', activebackground='#3D16DB',
						 fg='black', command=how_to_play_screen, font=("Arial Bold", 35))
    main_menu_canvas.create_window(650, 440, anchor='nw', window=how_to_play)

    settings_button = Button(window, text="Settings", bg='#c5f6f6', activebackground='#3D16DB',
							 fg='black', command=settings_screen, font=("Arial Bold", 35))
    main_menu_canvas.create_window(650, 540, anchor='nw', window=settings_button)

    quit = Button(window, text="Quit", bg='#c5f6f6', activebackground='#3D16DB', fg='black',
                  command=quit_the_game, font=("Arial Bold", 35))
    main_menu_canvas.create_window(650, 640, anchor='nw', window=quit)

    # the "game state file" is only read once
    if just_turned_on_the_game:
        read_game_state_file()

    # resume button will be 'normal' when the previous game was not finished
    if(state_of_the_last_game == 1):
        resume['state'] = 'normal'
    elif(state_of_the_last_game == 0):
        resume['state'] = 'disabled'


def destroy_menu_items(canvas):
    items = canvas.winfo_children()
    for item in items:
        item.destroy()


def resume_button_pressed():
    global resume_button
    resume_button = True
    start()


def read_game_state_file():
    global state_of_the_last_game, resume_button, score, lives
    global time_period, coefficient_of_falling

    resume_button = False

    state_file = open("Data/save_game_state.txt", "r")
    text2 = state_file.readlines()

    # if empty
    if not text2:
        state_of_the_last_game = 0
    else:
        state_of_the_last_game = int(text2[0].rstrip())

    if(state_of_the_last_game == 1):
        resume['state'] = 'normal'
        # get the values from the last game so the game can be continued
        score = int(text2[1].rstrip())
        lives = int(text2[2].rstrip())
        time_period = int(text2[3].rstrip())
        coefficient_of_falling = float(text2[4].rstrip())
    elif(state_of_the_last_game == 0):
        resume['state'] = 'disabled'

    state_file.close()


def quit_the_game():
    write_to_game_state_file()
    window.destroy()


def write_to_game_state_file():
    global state_of_the_last_game

    state_file = open("Data/save_game_state.txt", "w")

    if (state_of_the_last_game == 1):
        state_file.write('1\n')
        state_file.write(str(score))
        state_file.write('\n')
        state_file.write(str(lives))
        state_file.write('\n')
        state_file.write(str(time_period))
        state_file.write('\n')
        state_file.write(str(coefficient_of_falling))
    elif(state_of_the_last_game == 0):
        state_file.write('0')

    state_file.close()

# providing some information on how to play this game for a beginner
def how_to_play_screen():
    destroy_menu_items(window)

    how_to_play_canvas = Canvas(window, width=width, height=height)
    how_to_play_canvas.pack(fill="both", expand=True)

    how_to_play_canvas.create_image(0, 0, image=bg4, anchor='nw')

    text = 'The purpose of the game is to catch as many eggs as possible using a brown box which is\ncontrolled by default using arrow keys to left (<-) and right (->). '
    how_to_play_canvas.create_text(888, 100, text=text,  fill='black', font=("Arial Bold", 20))

    text = '\nThe pause can be turned on by the Escape keyboard button (default). What is more, you are\n free to turn off the game even if you have not finished playing, as the game state is saved.'
    how_to_play_canvas.create_text(900, 190, text=text,  fill='black', font=("Arial Bold", 20))

    text = '\nAlso, there is included a boss key which can be activated using the b keyboard button (default). To leave that\nmode you need to find a small button Resume which is at the top of the screen.'
    how_to_play_canvas.create_text(765, 300, text=text,  fill='black', font=("Arial Bold", 20))

    text = '\nAs you progress the game becomes more difficult. Per 20 new points, you receive an extra life.'
    how_to_play_canvas.create_text(1300, 400, text=text, anchor='e', fill='black', font=("Arial Bold", 20))

    text = '\nThe best five players are included in the leaderboards, this is how you can monitor your progress. Practice\nmakes perfect! Good luck!'
    how_to_play_canvas.create_text(1450, 500, text=text, anchor='e', fill='black', font=("Arial Bold", 20))

    get_back_to_menu = Button(how_to_play_canvas, text="Get back to menu", bg='#c5f6f6',
    						  activebackground='#3D16DB', fg='black', command=menu_contents, font=("Arial Bold", 35))
    how_to_play_canvas.create_window(580, 600, anchor='nw', window=get_back_to_menu)


def settings_screen():
	destroy_menu_items(window)

	settings_canvas = Canvas(window, width=width, height=height)
	settings_canvas.pack(fill="both", expand=True)

	settings_canvas.create_image(0, 0, image=bg4, anchor='nw')

	change_name = Button(settings_canvas, width=21, height=1, text="Change your name", bg='#c5f6f6',
						 activebackground='#3D16DB', fg='black', font=("Arial Bold", 40), command=change_your_name)
	settings_canvas.create_window(415, 220, anchor='nw', window=change_name)

	change_buttons = Button(settings_canvas, width=21, height=1, text="Change keyboard buttons", bg='#c5f6f6',
				 			activebackground='#3D16DB', fg='black', font=("Arial Bold", 40), command=change_keyboard_buttons)
	settings_canvas.create_window(415, 350, anchor='nw', window=change_buttons)

	get_back_to_menu = Button(settings_canvas, text="Get back to menu", bg='#c5f6f6', activebackground='#3D16DB',
							  fg='black', command=leave_settings_screen, font=("Arial Bold", 35))
	settings_canvas.create_window(565, 600, anchor='nw', window=get_back_to_menu)


def change_your_name():
	global name, get_name, settings, change_name_canvas, old_name

	# settings screen is on
	settings = True

	destroy_menu_items(window)

	# saving an old name in case a new one is invalid or an empty string
	old_name = name

	change_name_canvas = Canvas(window, width=width, height=height)
	change_name_canvas.pack(fill="both", expand=True)

	change_name_canvas.create_image(0, 0, image=bg4, anchor='nw')

	change_name_canvas.create_text(788, 100, text="Change your name", justify='center', fill='black',
								   font=("Arial Bold", 40))

	get_name = Entry(change_name_canvas, font=("Arial Bold", 25), bg='#c5f6f6')
	change_name_canvas.create_window(580, 150, anchor='nw', window=get_name)

	changing_the_name = Button(change_name_canvas, text="Change your name", bg='#c5f6f6',
							   activebackground='#3D16DB', fg='black', font=("Arial Bold", 30), command=get_the_name)
	change_name_canvas.create_window(586, 300, anchor='nw', window=changing_the_name)

	get_back_to_menu = Button(change_name_canvas, text="Get back to menu", bg='#c5f6f6',
							  activebackground='#3D16DB', fg='black', command=leave_settings_screen, 
							  font=("Arial Bold", 35))
	change_name_canvas.create_window(565, 600, anchor='nw', window=get_back_to_menu)


def change_keyboard_buttons():
	global change_keyboard_buttons_canvas, moving_to_left, moving_to_right, new_pause_button, new_boss_key
	destroy_menu_items(window)

	change_keyboard_buttons_canvas = Canvas(window, width=width, height=height)
	change_keyboard_buttons_canvas.pack(fill="both", expand=True)

	change_keyboard_buttons_canvas.create_image(0, 0, image=bg4, anchor='nw')
	
	change_keyboard_buttons_canvas.create_text(788, 100, text="Define your keys", justify='center',
											   fill='black', font=("Arial Bold",40))

	moving_to_left = Button(change_keyboard_buttons_canvas, height=1, width=19, text="Move the object to left",
							bg='#c5f6f6', activebackground='#3D16DB', fg='black', font=("Arial Bold", 30),
							command=moving_to_left_pressed)
	change_keyboard_buttons_canvas.create_window(515, 300, window=moving_to_left)
	
	moving_to_right = Button(change_keyboard_buttons_canvas, height=1, width=19, text="Move the object to right",
							 bg='#c5f6f6', activebackground='#3D16DB', fg='black', font=("Arial Bold", 30),
							 command=moving_to_right_pressed)
	change_keyboard_buttons_canvas.create_window(1060, 300, window=moving_to_right)
	
	new_pause_button = Button(change_keyboard_buttons_canvas, height=1, width=19, text="Pause", bg='#c5f6f6',
							  activebackground='#3D16DB', fg='black', font=("Arial Bold", 30), 
							  command=new_pause_button_pressed)
	change_keyboard_buttons_canvas.create_window(515, 500, window=new_pause_button)
	
	new_boss_key = Button(change_keyboard_buttons_canvas, height=1, width=19, text="Boss key", bg='#c5f6f6',
						  activebackground='#3D16DB', fg='black', font=("Arial Bold", 30),
						  command=new_boss_key_pressed)
	change_keyboard_buttons_canvas.create_window(1060, 500, window=new_boss_key)

	get_back_to_menu = Button(change_keyboard_buttons_canvas, text="Get back to menu", bg='#c5f6f6',
							  activebackground='#3D16DB', fg='black', command=leave_settings_screen, 
							  font=("Arial Bold",35))
	change_keyboard_buttons_canvas.create_window(565, 600, anchor='nw', window=get_back_to_menu)


# check if all keyboard buttons are unique, that is, there are not any duplicates
def no_duplicates_in_buttons(index, value, button):
	warning = change_keyboard_buttons_canvas.create_text(788, 400, text="", justify='center',
														 fill='black', font=("Arial Bold", 30))

	if value in controls:
		if value != controls[index]:
			change_keyboard_buttons_canvas.itemconfigure(warning, 
														 text='You cannot have one key for two different ' +
														 	  'operations!\n Please select another one')

	else:
		controls[index] = value
		button['text'] = controls[index]
		updating_control_buttons()


def moving_to_left_pressed():
	moving_to_right['text'] = "Move the object to right"
	new_pause_button['text'] = "Pause"
	new_boss_key['text'] = "Boss key"

	window.unbind("<Key>")
	moving_to_left['text'] = controls[0]
	window.bind("<Key>", change_the_button_for_moving_to_left)


def change_the_button_for_moving_to_left(event):
	value = event.keysym
	no_duplicates_in_buttons(0, value, moving_to_left)


def moving_to_right_pressed():
	moving_to_left['text'] = "Move the object to left"
	new_pause_button['text'] = "Pause"
	new_boss_key['text'] = "Boss key"

	window.unbind("<Key>")
	moving_to_right['text'] = controls[1]
	window.bind("<Key>", change_the_button_for_moving_to_right)


def change_the_button_for_moving_to_right(event):
	value = event.keysym
	no_duplicates_in_buttons(1, value, moving_to_right)
	

def new_pause_button_pressed():
	moving_to_right['text'] = "Move the object to right"
	moving_to_left['text'] = "Move the object to left"
	new_boss_key['text'] = "Boss key"

	window.unbind("<Key>")
	new_pause_button['text'] = controls[2]
	window.bind("<Key>", change_the_button_for_pause)


def change_the_button_for_pause(event):
	value = event.keysym
	no_duplicates_in_buttons(2,value, new_pause_button)


def new_boss_key_pressed():
	moving_to_right['text'] = "Move the object to right"
	moving_to_left['text'] = "Move the object to left"
	new_pause_button['text'] = "Pause"

	window.unbind("<Key>")
	new_boss_key['text'] = controls[3]
	window.bind("<Key>", change_the_button_for_boss_key)


def change_the_button_for_boss_key(event):
	value = event.keysym
	no_duplicates_in_buttons(3, value, new_boss_key)


def leave_settings_screen():
	window.unbind("<Key>")
	menu_contents()


# 'start' button is pressed on the menu and the game is started
def start():
	global game_canvas, resume_button, stop_making_eggs, not_append_but_to_read_leaderboards
	global just_turned_on_the_game, boss_key_turned_on
	global boss_key_mode, pause, stop, size_of_egg, score, pause_turned_on, score_text, lives
	global lives_text, coefficient_of_falling, main_object, size_of_object, time_period

	destroy_menu_items(window)

	menu_is_on = False
	just_turned_on_the_game = False
	not_append_but_to_read_leaderboards = False

	# the size of an egg is 20x29 px
	size_of_egg = [20, 29] 

	size_of_object = 192

	pause_turned_on = False
	pause = False

	boss_key_turned_on = False
	boss_key_mode = False

	stop = False
	stop_making_eggs = False

	# default parameters when there is no saved data or 'resume' button is not pressed
	if (state_of_the_last_game == 0 or not resume_button):
		score = 0
		lives = 5
		time_period = 90

		# determines how fast the egg is falling 
		coefficient_of_falling = 1

	resume_button = False

	game_canvas = Canvas(window, width=width, height=height)
	game_canvas.pack(fill="both", expand=True)

	game_canvas.create_image(0, 0, image=bg3, anchor='nw')

	score_txt = "Score: " + str(score)
	score_text = game_canvas.create_text(width/4 , 35 , fill="black", font="Times 40 italic bold", 
				 						 text=score_txt)

	lives_txt = "Lives: " + str(lives)
	lives_text = game_canvas.create_text(width*3/4 , 35 , fill="black", font="Times 40 italic bold", 
										 text=lives_txt)

	main_object = game_canvas.create_rectangle(width/2-size_of_object/2, height-size_of_object, 
											   width/2+size_of_object/2, height, fill="#69351B")

	# initiate functions controlling the flow of the game
	control_of_main_object()
	generate_an_egg()


def control_of_main_object():
	global game_canvas, pause, boss_key_mode, only_to_right, only_to_left, main_object_position

	# determining if the object reached the end of the screen window (max right or left side)
	only_to_right = False
	only_to_left = False

	window.title("Eggs Collection Simulator")

	# main controls of the game
	# they can be changed by a player as well
	game_canvas.bind("<" + controls[0] +">", move_to_left)
	game_canvas.bind("<" + controls[1] +">", move_to_right)
	game_canvas.bind("<" + controls[2] +">", pause_the_game)

	# cheating codes
	game_canvas.bind("<l><i><f><e>", add_lives_cheat)
	game_canvas.bind("<Control-C>", decrease_lives_cheat)
	game_canvas.bind("<s><l><o><w>", slow_the_game_cheat)

	# for turning on a 'boss key'
	# there is a small button at the top of the image 'resume' to get back to the game
	game_canvas.bind("<" + controls[3] +">", working_screen_on)

	game_canvas.focus_set()

	# determining the position of the main object
	main_object_position = game_canvas.coords(main_object)

	# determining if the object reached the end of the screen window (max right or left side)
	if (main_object_position[0] >= 0 and main_object_position[0] < size_of_object/2):
		only_to_right = True
	elif (main_object_position[2] > width-size_of_object/2 and main_object_position[2] <= width):
		only_to_left = True


# move the object to left
def move_to_left(event):
	if not only_to_right and not pause and not stop and not boss_key_mode:
		only_to_left = False
		if not only_to_right:
			game_canvas.coords(main_object, main_object_position[0]-size_of_object/2, 
							   main_object_position[1], main_object_position[2]-size_of_object/2,
							   main_object_position[3])

	control_of_main_object()


# move the object to right
def move_to_right(event):
	if not only_to_left and not pause and not stop and not boss_key_mode:
		only_to_right = False
		if not only_to_left:
			game_canvas.coords(main_object, main_object_position[0]+size_of_object/2, 
							   main_object_position[1], main_object_position[2]+size_of_object/2, 
							   main_object_position[3])

	control_of_main_object()


def pause_the_game(event):
	global temp_canvas, pause, pause_turned_on

	if not pause_turned_on and not boss_key_turned_on:
		pause = True
		pause_turned_on = True

		game_canvas.pack_forget()

		temp_canvas = Canvas(window, width=width, height=height)
		temp_canvas.pack(fill="both", expand=True)

		temp_canvas.create_image(0, 0, image=bg, anchor='nw')

		unpause_game = Button(temp_canvas, text="Resume", bg='#c5f6f6', activebackground='#3D16DB',
							  fg='black', font=("Arial Bold", 35), command=get_back_to_game)
		unpause_game.pack(pady=(80, 40))

		get_back_to_menu = Button(temp_canvas, text="Get back to the menu", bg='#c5f6f6', 
								  activebackground='#3D16DB', fg='black', font=("Arial Bold", 35), 
								  command=get_back_to_menu_button_pressed)
		get_back_to_menu.pack(pady=40)

		quit = Button(temp_canvas, text="Quit the game", bg='#c5f6f6', activebackground='#3D16DB', 
					  fg='black', command=quit_the_game_from_the_pause_menu, font=("Arial Bold", 35))
		quit.pack(pady=40)


# this functions is called from a button 'get_back_to_menu' from the pause screen
def get_back_to_menu_button_pressed():
	global state_of_the_last_game, game_canvas

	game_canvas.destroy()

	state_of_the_last_game = 1

	write_to_game_state_file()
	menu_contents()


# saves the game state to resume playing the next time
def quit_the_game_from_the_pause_menu():
	global state_of_the_last_game

	# saving the game state before quitting the game
	state_file = open("Data/save_game_state.txt", 'w')

	state_file.write('1\n')
	state_file.write(str(score))
	state_file.write('\n')
	state_file.write(str(lives))
	state_file.write('\n')
	state_file.write(str(time_period))
	state_file.write('\n')
	state_file.write(str(coefficient_of_falling))

	state_file.close()
	window.destroy()


def get_back_to_game():
	global temp_canvas, pause, pause_turned_on
	global working_canvas, boss_key_mode, boss_key_turned_on

	if pause:
		temp_canvas.pack_forget()
		pause = False
		pause_turned_on = False

	if boss_key_mode:
		working_canvas.pack_forget()
		boss_key_mode = False
		boss_key_turned_on = False

	game_canvas.pack(fill="both", expand=True)
	control_of_main_object()


# when boss key is pressed 
def working_screen_on(event):
	global working_canvas, boss_key_mode, boss_key_turned_on, game_canvas

	if not boss_key_turned_on and not pause_turned_on:
		boss_key_mode = True
		boss_key_turned_on = True

		window.title("")

		game_canvas.pack_forget()

		working_canvas = Canvas(window, width=width, height=height)
		working_canvas.pack(fill="both", expand=True)

		working_canvas.create_image(0, 0, image=excel_image, anchor='nw')

		resume_playing = Button(working_canvas, text="Resume", bg='#f3f2f1', bd=0, fg='#7c7b7a', 
								activeforeground='#7c7b7a', font=("Arial Bold", 11), command=get_back_to_game)
		resume_playing.pack(pady=47)


def add_lives_cheat(event):
	global lives

	lives += 1
	txt = "Lives: " + str(lives)
	game_canvas.itemconfigure(lives_text, text=txt)

	# save the new number of lives in the file
	write_to_game_state_file()


def decrease_lives_cheat(event):
	decrease_lives()

	# save the new number of lives in the file
	write_to_game_state_file()

	if (lives <= 0): 
		stop = True
		process_game_over()
		stop_making_eggs = True


def slow_the_game_cheat(event):
	global time_period, coefficient_of_falling

	# increase the time between generating two eggs
	if time_period > 80 and time_period < 1000:
		time_period += 5

	if coefficient_of_falling - 10 > 1:
		coefficient_of_falling -= 10
	elif coefficient_of_falling - 5 > 1:
		coefficient_of_falling -= 5
	elif coefficient_of_falling - 2 > 1:
		coefficient_of_falling -= 2
	elif coefficient_of_falling - 1 > 1:
		coefficient_of_falling -= 1

	# save the new difficulty level in the file
	write_to_game_state_file()


def generate_an_egg():
	global egg_object_position, egg_object, menu_is_on, state_of_the_last_game, time_period
	global coefficient_of_falling, stop

	state_of_the_last_game = 1
	
	try:
		x, y = generate_random_position()
		colour = generate_random_colour()

		write_to_game_state_file()

		egg_object = game_canvas.create_oval(x-size_of_egg[0], y-size_of_egg[1], x, y, fill=colour)

		while True:
			egg_object_position = game_canvas.coords(egg_object)

			# when the egg reaches the surface
			if egg_object_position[3] > height+10:
				game_canvas.delete(egg_object)
				decrease_lives()

				if (lives <= 0):
					game_over = True
					stop = True
					process_game_over()

				break

			if (overlapping()):
				game_canvas.delete(egg_object)
				increase_the_score()
				break

			if not pause and not boss_key_mode:
				game_canvas.move(egg_object, 0, 2)

				sleep(0.01/coefficient_of_falling)
				coefficient_of_falling += 0.0008

			window.update()
	
		if not pause and not boss_key_mode and not stop_making_eggs:
			increasing_game_difficulty()

		if 'game_over' not in locals() and not stop_making_eggs:
			window.after(time_period, generate_an_egg)

	except:
		pass


def overlapping():
	if main_object_position[0] < egg_object_position[2] and main_object_position[2] > egg_object_position[0] and main_object_position[1] < egg_object_position[3] and main_object_position[3] > egg_object_position[1]:
		
		return True

	return False


def generate_random_position():
	x_pos = randint(30, width-30)
	y_pos = randint(0, 10)
	return x_pos, y_pos


def generate_random_colour():
	hex_chars = '0123456789ABCDEF'
	colour = ''

	# 6 chars in the RGB
	for i in range(6):
		colour += hex_chars[randint(0, len(hex_chars)-1)]

	return '#' + colour


def increase_the_score():
	global score

	score += 1
	txt = "Score: " + str(score)
	game_canvas.itemconfigure(score_text, text=txt)
	add_new_lives()


def add_new_lives():
	global lives

	if (score % 20 == 0):
		lives += 1
		txt = "Lives: " + str(lives)
		game_canvas.itemconfigure(lives_text, text=txt)


def decrease_lives():
	global lives
	lives -= 1
	txt = "Lives: " + str(lives)
	game_canvas.itemconfigure(lives_text, text=txt)
	

def increasing_game_difficulty():
	global time_period, main_object, coefficient_of_falling

	time_period += 2

	if (score % 20 == 0 and score != 0):
		time_period += 5
		coefficient_of_falling += 0.75


def process_game_over():
	global state_of_the_last_game

	game_canvas.destroy()

	state_of_the_last_game = 0

	write_to_game_state_file()
	update_leaderboards()

	game_over_canvas = Canvas(window, width=width, height=height)
	game_over_canvas.pack(fill="both", expand = True)

	game_over_canvas.create_image(0, 0, image=bg2, anchor='nw')

	game_over_canvas.create_text(760, 80, text="GAME OVER", justify='center', fill='red', 
								 font=("Arial Bold", 40))
	game_over_canvas.create_text(760, 280, text="Your final score: " + str(score), justify='center', 
								 fill='blue', font=("Arial Bold", 40))

	play_again = Button(game_over_canvas, text="Play again", bg='#c5f6f6', activebackground='#3D16DB', 
						fg='black', font=("Arial Bold", 35), command=start)
	game_over_canvas.create_window(635, 340, anchor='nw', window=play_again)

	get_back_to_menu = Button(game_over_canvas, text="Get back to the menu", bg='#c5f6f6', 
							  activebackground='#3D16DB', fg='black', font=("Arial Bold", 35), command=menu_contents)
	game_over_canvas.create_window(490, 440, anchor='nw', window=get_back_to_menu)

	leaderboards = Button(game_over_canvas, text="See leaderboards", bg='#c5f6f6', activebackground='#3D16DB', 
						  fg='black', font=("Arial Bold", 35), command=show_leaderboards)
	game_over_canvas.create_window(542, 540, anchor='nw', window=leaderboards)

	quit = Button(game_over_canvas, text="Quit the game", bg='#c5f6f6', activebackground='#3D16DB', 
			      fg='black', command=quit_the_game, font=("Arial Bold", 35))
	game_over_canvas.create_window(580, 640, anchor='nw', window=quit)


def update_leaderboards():
	not_append_but_to_read_leaderboards = False

	read_the_leaderboards_file()
	write_to_the_leaderboards_file()
	

def read_the_leaderboards_file():
	global size_of_leaderboard_list, just_turned_on_the_game, text, names, scores, leaderboards_file

	leaderboards_file = open("Data/leaderboards.txt", "r")
	text = leaderboards_file.readlines()

	names = []
	scores = []

	size_of_leaderboard_list = int(len(text)/2)

	update_information_from_the_leaderboards_file()

	leaderboards_file.close()


def update_information_from_the_leaderboards_file():
	global size_of_leaderboard_list, just_turned_on_the_game

	if (size_of_leaderboard_list == 0):
		if not just_turned_on_the_game and not not_append_but_to_read_leaderboards:
			names.append(name)
			scores.append(str(score))
			size_of_leaderboard_list += 1

	elif (size_of_leaderboard_list < 5):
		if not just_turned_on_the_game and not not_append_but_to_read_leaderboards:
			text.append(name)
			text.append(score)
			size_of_leaderboard_list += 1

		get_the_sorted_list_of_names_and_scores()

	elif (size_of_leaderboard_list == 5):
		get_the_sorted_list_of_names_and_scores()

		the_score_of_5_best_player = int(scores[4])

		if (the_score_of_5_best_player <= score and not not_append_but_to_read_leaderboards):
			names[4] = name
			scores[4] = str(score)
			get_the_sorted_list_of_names_and_scores()
	else:
		messagebox.showwarning(title='Error!', message='Error! There can be only 5 names in the ' + 
													   'leaderboard list! Fix that issue!')
		
		size_of_leaderboard_list = 5

		get_the_sorted_list_of_names_and_scores()
		write_to_the_leaderboards_file()

		window.destroy()


def get_the_sorted_list_of_names_and_scores():
	global names, scores, size_of_leaderboard_list, text

	for i in range(2*size_of_leaderboard_list):
		text[i] = str(text[i]).rstrip()
		if (i % 2 == 0):
			names.append(text[i])
		elif (i % 2 != 0):
			scores.append(text[i])

	# converting from string to int
	scores = [int(i) for i in scores] 

	# take the use of optimized Bubble sort method to sort the players in the list
	for i in range(size_of_leaderboard_list-1):
		for j in range(size_of_leaderboard_list-i-1):

			if (scores[j] < scores[j+1]):
				scores[j], scores[j+1] = scores[j+1], scores[j]
				names[j], names[j+1] = names[j+1], names[j]

	# converting from int to string
	scores = [str(i) for i in scores] 


def write_to_the_leaderboards_file():
	file = open("Data/leaderboards.txt", "w")

	for i in range(size_of_leaderboard_list):
		file.write(names[i])
		file.write('\n')
		file.write(scores[i])
		file.write('\n')

	file.close()


# show the leaderboards list on the screen
def show_leaderboards():
	global size_of_leaderboard_list, not_append_but_to_read_leaderboards, score
	global just_turned_on_the_game, names, scores 

	if just_turned_on_the_game:
		score = 0

	not_append_but_to_read_leaderboards = True

	destroy_menu_items(window)

	leaderboards_canvas = Canvas(window, width=width, height=height)
	leaderboards_canvas.pack(fill="both", expand = True)

	leaderboards_canvas.create_image(0, 0, image=bg2, anchor='nw')

	leaderboards_canvas.create_text(790, 60, text="Leaderboards", justify='center', fill='black', 
									font=("Arial Bold", 50))

	read_the_leaderboards_file()

	# handle the cases when there are less or equal to 5 players
	if (size_of_leaderboard_list == 0):
		pass
	elif (size_of_leaderboard_list == 1):
		leaderboards_canvas.create_text(650, 200, text='1.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 200, text=names[0], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 200, text=scores[0], fill='black', anchor='w', font=("Arial Bold", 40))

	elif (size_of_leaderboard_list == 2):
		leaderboards_canvas.create_text(650, 200, text='1.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 200, text=names[0], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 200, text=scores[0], fill='black', anchor='w', font=("Arial Bold", 40))

		leaderboards_canvas.create_text(650, 270, text='2.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 270, text=names[1], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 270, text=scores[1], fill='black', anchor='w', font=("Arial Bold", 40))

	elif (size_of_leaderboard_list == 3):
		leaderboards_canvas.create_text(650, 200, text='1.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 200, text=names[0], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 200, text=scores[0], fill='black', anchor='w', font=("Arial Bold", 40))

		leaderboards_canvas.create_text(650, 270, text='2.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 270, text=names[1], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 270, text=scores[1], fill='black', anchor='w', font=("Arial Bold", 40))
		
		leaderboards_canvas.create_text(650, 340, text='3.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 340, text=names[2], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 340, text=scores[2], fill='black', anchor='w', font=("Arial Bold", 40))

	elif (size_of_leaderboard_list == 4):
		leaderboards_canvas.create_text(650, 200, text='1.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 200, text=names[0], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 200, text=scores[0], fill='black', anchor='w', font=("Arial Bold", 40))

		leaderboards_canvas.create_text(650, 270, text='2.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 270, text=names[1], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 270, text=scores[1], fill='black', anchor='w', font=("Arial Bold", 40))
		
		leaderboards_canvas.create_text(650, 340, text='3.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 340, text=names[2], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 340, text=scores[2], fill='black', anchor='w', font=("Arial Bold", 40))
		
		leaderboards_canvas.create_text(650, 410, text='4.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 410, text=names[3], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 410, text=scores[3], fill='black', anchor='w', font=("Arial Bold", 40))

	elif (size_of_leaderboard_list == 5):
		leaderboards_canvas.create_text(650, 200, text='1.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 200, text=names[0], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 200, text=scores[0], fill='black', anchor='w', font=("Arial Bold", 40))

		leaderboards_canvas.create_text(650, 270, text='2.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 270, text=names[1], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 270, text=scores[1], fill='black', anchor='w', font=("Arial Bold", 40))
		
		leaderboards_canvas.create_text(650, 340, text='3.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 340, text=names[2], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 340, text=scores[2], fill='black', anchor='w', font=("Arial Bold", 40))
		
		leaderboards_canvas.create_text(650, 410, text='4.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 410, text=names[3], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 410, text=scores[3], fill='black', anchor='w', font=("Arial Bold", 40))
		
		leaderboards_canvas.create_text(650, 480, text='5.', fill='black', anchor='e', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(670, 480, text=names[4], fill='black', anchor='w', font=("Arial Bold", 40))
		leaderboards_canvas.create_text(1310, 480, text=scores[4], fill='black', anchor='w', font=("Arial Bold", 40))

	get_back_to_menu = Button(leaderboards_canvas, text="Get back to menu", bg='#c5f6f6', 
							  activebackground='#3D16DB', fg='black', command=menu_contents, font=("Arial Bold", 35))
	leaderboards_canvas.create_window(580, 540, anchor='nw', window=get_back_to_menu)



# The beginning of the code
window = Tk()
configure_window()

# default keyboard buttons
controls = ['Left', 'Right', 'Escape', 'b']
score = 0

getting_control_buttons()

# link for the source of the photo: 
# https://pixabay.com/illustrations/landscape-vector-nature-house-farm-1617449/
bg = PhotoImage(file='Images/background_1.png')

# these are the edited versions of the original one above
# it is allowed to do according to the licence
bg2 = PhotoImage(file='Images/background_2.png')
bg3 = PhotoImage(file='Images/background_3.png')
bg4 = PhotoImage(file='Images/background_4.png')
bg5 = PhotoImage(file='Images/background_5.png')

# the image was made by me
excel_image = PhotoImage(file='Images/excel_image.png')

ask_for_name_first_time()

window.mainloop()
