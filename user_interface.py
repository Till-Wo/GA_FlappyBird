from tkinter import *
from CONSTANTS import VARIABLES, POPULATION_SIZE


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def positive(number):
    if number >= 0:
        return number
    else:
        return -number


def space_value(name, value):
    space = ""
    for _ in range(30 - len(name)):
        space += " "
    return f"{name}:{space}{value}"


def apply_button():
    from CONSTANTS import VARIABLES
    VARIABLES.mutation_strength = mutation_slider.get()
    VARIABLES.speed = speed_slider.get()
    VARIABLES.learing_rate = learning_slider.get()
    VARIABLES.crossover_active = crossover_active.get()


def save_button():
    VARIABLES.population.population.sort(key=lambda x: x.score)
    VARIABLES.population.population[-1].NN.save(
        r"C:\Users\tillw\Desktop\MATURA_PROJEKT\Evolutionary_Algorithm\TestProjects\Flappy_Example\Saved_Nets\net.txt")


def load_button():
    VARIABLES.population.population[-1].NN.load(
        r"C:\Users\tillw\Desktop\MATURA_PROJEKT\Evolutionary_Algorithm\TestProjects\Flappy_Example\Saved_Nets\net.txt")


def kill_button():
    if VARIABLES.population is not None:
        for i in VARIABLES.population.population:
            i.alive = False


def next_button():
    global active
    active += 1

    if active > POPULATION_SIZE - 1:
        active = 0
    select_slider.set(active)


def previous_button():
    global active
    active -= 1

    if active < 0:
        active = POPULATION_SIZE - 1
    select_slider.set(active)


def last_button():
    global active
    active = POPULATION_SIZE - 1
    select_slider.set(active)


def first_button():
    global active
    active = 0
    select_slider.set(active)


def input_active_return(trash):
    global active
    try:
        new = int(input_active.get())
        active = new if 0 <= new < POPULATION_SIZE else active
    except:
        print("NAN")
    input_active.delete(0, 'end')
    select_slider.set(active)


def find_alive_button():
    global active
    if VARIABLES.population is not None:
        for i, individual in enumerate(VARIABLES.population.population):
            if individual.alive:
                active = i
    select_slider.set(active)


def update_individual_info():
    individual_active.set(space_value("Active: ", active))
    individual_alive.set(space_value("Alive: ", VARIABLES.population.population[active].alive))
    individual_reached_pilars.set(space_value("Reached: ", VARIABLES.population.population[active].reached_pilars))
    individual_score.set(space_value("Survived Ticks: ", VARIABLES.population.population[active].score))


def draw_net():
    value_list = []
    pax, pay, pbx, pby = [], [], [], []
    y_input, y_output, x_output, x_input = 0, 0, 0, 0
    weights = VARIABLES.population.population[active].NN.get_unflattend()
    for i, layer in enumerate(weights):
        x_output += 300 / len(weights)
        y_input = 0
        for j, neurons in enumerate(layer):
            y_output = 0
            y_input += 300 / (len(layer) + 1)
            for l, neuron in enumerate(neurons):
                y_output += 300 / (len(neurons) + 1)
                value_list.append(neuron)
                pax.append(x_input + 10)
                pay.append(y_input + 10)
                pbx.append(x_output + 10)
                pby.append(y_output + 10)

        x_input += 300 / len(weights)

    max_value_list = [positive(x) for x in value_list]
    maximum = max(max_value_list)
    display.delete("all")
    for i in range(len(pax)):
        if value_list[i] >= 0:
            color = (0, 255 - int((value_list[i] / maximum) * 255),
                     0)

        else:
            color = (255 - int((positive(value_list[i]) / maximum) * 255), 0,
                     0)
        display.create_line(pax[i], pay[i], pbx[i], pby[i], fill=_from_rgb(color),
                            width=2)


tk = Tk()
tk.title("Control Panel")
tk.geometry("600x600")
individual_active = StringVar()
individual_alive = StringVar()
individual_reached_pilars = StringVar()
individual_score = StringVar()
crossover_active = BooleanVar()
rightframe = Frame(tk)
rightframe.pack(side=RIGHT)
leftframe = Frame(tk)
leftframe.pack(side=LEFT, anchor=NW)
buttonframe = Frame(rightframe)

speed_slider = Scale(leftframe, from_=1, to=400, resolution=1, orient=HORIZONTAL, length=400, label="Speed:")
speed_slider.pack()
mutation_slider = Scale(leftframe, from_=0.0, to=1.0, resolution=0.01, orient=HORIZONTAL, length=200,
                        label="Mutation Strength:")
mutation_slider.set(VARIABLES.mutation_strength)
mutation_slider.pack()
learning_slider = Scale(leftframe, from_=0.0, to=1.0, resolution=0.01, orient=HORIZONTAL, length=200,
                        label="Learning Rate:")
learning_slider.set(VARIABLES.learing_rate)
learning_slider.pack()

crossover = Checkbutton(leftframe, text="Crossover", variable=crossover_active)
crossover.pack()
apply_btn = Button(leftframe, text="Apply", command=apply_button)
apply_btn.pack()
save_btn = Button(leftframe, text="Save", command=save_button)
save_btn.pack()

load_btn = Button(leftframe, text="Load", command=load_button)
load_btn.pack()
kill_btn = Button(leftframe, text="KILL ALL", command=kill_button)
kill_btn.pack()

individual_active_label = Label(rightframe, textvariable=individual_active)
individual_active_label.pack()
individual_alive_label = Label(rightframe, textvariable=individual_alive)
individual_alive_label.pack()
individual_reached_pilars_label = Label(rightframe, textvariable=individual_reached_pilars)
individual_reached_pilars_label.pack()
individual_score_label = Label(rightframe, textvariable=individual_score)
individual_score_label.pack()

active = 0
display = Canvas(rightframe, width=320, height=320, bg= "black")
display.pack()
buttonframe.pack()
first_btn = Button(buttonframe, text="<<", command=first_button)
first_btn.pack(side=LEFT)
left_btn = Button(buttonframe, text="<", command=previous_button)
left_btn.pack(side=LEFT)
input_active = Entry(buttonframe)
input_active.bind("<Return>", input_active_return)
input_active.pack(side=LEFT)
right_btn = Button(buttonframe, text=">", command=next_button)
right_btn.pack(side=LEFT)
last_btn = Button(buttonframe, text=">>", command=last_button)
last_btn.pack(side=LEFT)
select_slider = Scale(rightframe, from_=0, to=POPULATION_SIZE - 1, resolution=1, orient=HORIZONTAL, length=200)
select_slider.set(active)
select_slider.pack()
find_alive_btn = Button(rightframe, text="Find something alive!", command=find_alive_button)
find_alive_btn.pack()

counter = 0


def flip():
    global counter, active
    tk.update()
    if counter > VARIABLES.speed:
        counter = 0
        update_individual_info()
        draw_net()
        active = select_slider.get()
        VARIABLES.speed = speed_slider.get()
    else:
        counter += 1
